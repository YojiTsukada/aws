import boto3
import sys
import os


from account import *
print(AWS_ACCESS_KEY_ID)
print(AWS_SECRET_ACCESS_KEY)


client = boto3.client('rekognition','ap-northeast-1')

bucket = 'frombk'
name = 'P4060899.JPG'

response = client.detect_labels(
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': name,
        }
    }
)

print('Detecting .... Labels')
for label in response['Labels']:
    print(label['Name'] + " : " + str(label['Confidence']))