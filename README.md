# AWS Lambda for monitoring EC2 Instance State Changes

It is possible to configure a CloudWatch rule for EC2 instance state changes and directly associate with AWS SNS however if you choose that path, SNS message will show EC2 instance ID and it's almost impossible to know which server is actually started, stopped, terminated through that ID number.  

That's why I prefer getting that SNS nitification through AWS Lambda function, so we can get the actual server name.  
## Requirements
Lambda function will need IAM role with
	- arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
	- arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess
	- Custom SNS publish policy for target SNS topic 
## Output
```shell
Sample SNS message:
Instance: development-test-01 / i-00dc7daa6a199375f inside account: ABC now in new state: RUNNING Time: 2020-10-15 12:52:57.084672
```
