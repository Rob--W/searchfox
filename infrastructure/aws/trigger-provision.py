# trigger-provision.py <indexer-provision.sh | web-server-provision.sh>

import boto3
from datetime import datetime, timedelta
import sys
import os.path

provisioner = sys.argv[1]

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

script = open(provisioner).read()

user_data = '''#!/bin/bash

cat > ~ubuntu/provision.sh <<"FINAL"
{script}
FINAL

chmod +x ~ubuntu/provision.sh
sudo -i -u ubuntu ~ubuntu/provision.sh
'''.format(script=script)

# ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-20160815 (ami-f701cb97)
image_id = 'ami-f701cb97'

launch_spec = {
    'ImageId': image_id,
    'KeyName': 'Main Key Pair',
    'SecurityGroups': ['indexer'],
    'UserData': user_data,
    'InstanceType': 'c3.2xlarge',
    'BlockDeviceMappings': []
}

client.run_instances(MinCount=1, MaxCount=1, **launch_spec)
