from datetime import datetime, timedelta, timezone
import urllib.parse
import mimetypes
import sys
import boto3
  
def lambda_handler(event, context):

    # S3 Client
    s3 = boto3.resource('s3')
    
    # Timezone (JST)
    JST = timezone(timedelta(hours=+9), 'JST')

    # Set time
    now = datetime.now(JST)
    filename = now.strftime("lambda.log_%Y%m%d_%H%M%S")

    # Get FileName.
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8') 

    # Check MIME TYPE.
    bucket_name = 'frombk'
    s3.Bucket(bucket_name).download_file(key, '/tmp/file')
    mime = mimetypes.guess_type('/tmp/file')[0]

    # make Temporaly.
    with open('/tmp/tmp.log', "w") as file:
        message = key + "," + str(mime)  + "," +  str(now)
        file.write(message)

    # upload to S3
    bucket_name = 'detbk'
    s3.Bucket(bucket_name).upload_file('/tmp/tmp.log', filename)

    return  mime