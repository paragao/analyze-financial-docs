import json
import boto3
from urllib
import os
import sys
import uuid
from helper import FileHelper

# ADD your Textract client/resource here
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
    print("event: {}\n".format(event))

    request = {}
    request["bucketName"] = event['Records'][0]['s3']['bucket']['name']
    request["objectName"] = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    request["outpuBucket"] = os.environ('OUTPUT_BUCKET')

    ext = FileHelper.getFileExtenstion(request["objectName"].lower())

    # if the file is JPG and PNG we can make a synchronus call to Textract. If it is a PDF, it have to be asynchronous.     
    if (ext and ext in ["jpg", "jpeg", "png"]):
        #TODO: create your sync call here. 
        #use download_object(request) to download the object so you can send it to Textract

    else: 
        #TODO: create your async call here
        # use download_object(request) to download the object so you can send it to Textract


    print('saving Textract output in a separate prefix\n')
    #TODO: after Textract returns, either a sync or async call, upload the output to the same bucket but other prefix
    # use upload_object(request) to upload the object to the prefix
    # make sure you add the output of Textract in the request dict before calling upload_object(request)


    # should return 200 for the API Gateway. Body can be different, if required.
    return {
        'statusCode': 200,
        'body': 'Success!'
    }
