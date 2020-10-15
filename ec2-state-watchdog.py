# Get EC2 Instance state changes with date and server name
# Sends SNS notification
# Fehmi-10/20

import json
import boto3
import time
import os

#
vAccountName="ABC"
#

def lambda_handler(event, context):
    print(context)
    # Create an SNS client
    worker_sns = boto3.client('sns')
    
    # Create an EC2 client
    worker_ec2 = boto3.client('ec2')
    
    #Fix local time
    os.environ['TZ'] = 'US/Eastern'
    time.tzset()
    # Info that we need to know
    vNow=time.strftime('%X %x %z')
    vInstanceId=event['detail']['instance-id']
    vInstanceState=event['detail']['state']
    
    # Try to find EC2 instance name
    response = worker_ec2.describe_instances( InstanceIds=[vInstanceId,],)
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            try:
                for item in instance["Tags"]:
                    if item['Key'] == 'Name':
                        vInstanceName=item['Value']
            except KeyError as e:
                    print(f' Instance {vInstanceId} has NO Name tag ')
                    vInstanceName="NoNameTag"
    
    vMessage="Instance: " +  vInstanceName + " / " + vInstanceId + " inside account: " + vAccountName +  " now in new state: " + vInstanceState.upper() + " Time: " + str(vNow)
    
    # Publish a simple message to the specified SNS topic
    response = worker_sns.publish(
        TopicArn='arn:aws:sns:us-east-1:111111111111:ops-alert',
        Subject='EC2 State Change',
        Message=vMessage,    
    )
