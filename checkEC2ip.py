import boto3


ec2 = boto3.resource('ec2')
sec = boto3.client('ec2').describe_security_groups()
mylist = []
running = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])



for instance in ec2.instances.all():

	
	for tag in instance.tags:
		if 'Name'in tag['Key']:
			name = tag['Value']
	
	for group in instance.security_groups:
		groupId = group['GroupId']
		for group in sec['SecurityGroups']:
			if group['GroupId'] == groupId:
				for permission in group['IpPermissions']:
					ipR = permission['IpRanges']
					for ip in ipR: 
						if ip['CidrIp'] == '0.0.0.0/0':
							print "It looks like %s (id %s) is open on port %d" % (name, instance.instance_id, permission['FromPort']) 
							if instance not in running:
								print "Don't worry too much though, this instace isn't running."
							else:
								print "Worse still, this instance is running"
