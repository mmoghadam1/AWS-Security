import boto3, json

s3 = boto3.resource('s3')
client = boto3.client('s3')
mylist = []
for i in s3.buckets.all():
	name = i.name
	acl = i.Acl()					# Check acl of bucket
	for grant in acl.grants:
		if grant['Grantee']['Type'].lower() == 'group' \
		   and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
		   mylist.append(name)		#Bucket is public
		else:
			continue				#Bucket is not public
	
	bp = s3.BucketPolicy(name)		#check policy of bucket
	try:
		pobj = bp.policy
	except Exception as e: 			#except if
		continue					#bucket has no policy
	policy = json.loads(pobj)
	if 'Statement' in policy:
		for p in policy['Statement']:
			if p['Principal'] == '*':
				mylist.append(name)	
				# print p['Action']

myset = set(mylist)					#convert to set to get unique buckets
print list(myset)