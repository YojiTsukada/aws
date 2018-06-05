import boto3
import sys
import os

# import account information.
from account import *

# setup s3 client.
s3 = boto3.resource('s3')

# setup rekognition client.
client = boto3.client('rekognition','ap-northeast-1')

# read a image.
bucket = 'frombk'
name = 'f.jpg'

# detect label.
response = client.detect_labels(
    Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': name,
        }
    }
)

# Download log 
dest_bucket = 'detbk'
logfile = "rekogniton.csv"

try:
    s3.Bucket(dest_bucket).download_file(logfile, '/tmp/' + logfile)
except:
    # make blank file
    with open('/tmp/' + logfile,"w"):pass    

# print result.
print('Detecting .... ' + name +  ' Labels')

with open('/tmp/' + logfile, "a") as file:
    file.write(name + ', ')
    for label in response['Labels']:
        print(label['Name'] + " : " + str(label['Confidence']))
        # write logfile.
        file.write(label['Name'] + ", " + str(label['Confidence']) + ", ")
    file.write('\n')


# upload to S3
s3.Bucket(dest_bucket).upload_file('/tmp/' + logfile, logfile)
