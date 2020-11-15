import json
import boto3
from urllib
import os
import sys
import uuid
import datastore 
from helper import FileHelper

s3 = boto3.client('s3')

def download_object(request):
    print("request: {}\n".format(request))
        
    bucket = request["bucketName"]
    key = request("objectName")

    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    
    print('downloading file\n')
    obj = s3.download_file(bucket, key, download_path)

    return obj

def upload_object(request, textractOutput):
    print("request: {}\n".format(request))

    bucket = request["bucketName"]
    output = textractOutput
    upload_path = '/tmp/textract-output-{}'.format(request["tempObject"])

    print('uploading file\n')
    obj = s3.upload_file(upload_path, '{}-output'.format(bucket), key)

    return obj 

def handler(event, context):
    print("event: {}".format(event))

    # get the name of the bucket and object from the event payload
    request = {}
    request["bucketName"] = event['Records'][0]['s3']['bucket']['name']
    request["objectName"] = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    request["outpuBucket"] = os.environ('OUTPUT_BUCKET')

    ext = FileHelper.getFileExtenstion(request["objectName"].lower())




    # should return 200 for the API Gateway. Body can be different, if required.
    return {
        'statusCode': 200,
        'body': 'Success!'
    }

