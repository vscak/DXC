import json
import os
import boto3

s3_client = boto3.resource('s3')
ssm_client = boto3.client('ssm')
parameter = os.environ['ssm_parameter']

def getssm_value():
    
    #function to get SSM parameter value
    ssm_response = ssm_client.get_parameter(Name=parameter)
    return ssm_response

def lambda_handler(event, context):
    
    ssm_value = {'Name':getssm_value()['Parameter']['Name'] , 'Value':getssm_value()['Parameter']['Value']}
    
    
    #converting SSM value as a json file
    
    with open('/tmp/param_value.json', 'w') as file:
        json.dump(ssm_value, file)
    
    #uploading the file to s3 bucket
    s3_client.meta.client.upload_file('/tmp/param_value.json', 'dxcparameter', 'param_value.json')