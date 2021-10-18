import json
import boto3
import urllib
import os
import sys
import uuid
import time

s3 = boto3.client('s3')
prefix = 'textract_output' # the prefix where files will be saved in the original bucket

# ADD your Textract and Comprehend client/resource here
##ANSWER:
textract = boto3.client('textract')
comprehend = boto3.client('comprehend')

def download_object(request):
    print("request: {}\n".format(request))
        
    bucket = request["bucketName"]
    key = request["objectName"]

    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    
    print('downloading file\n')
    s3.download_file(bucket, key, download_path)

    return download_path

def upload_object(request, response, name=None):
    print("request: {}\n".format(request))
    keyNoExt = os.path.splitext(request["objectName"].lower())[0].split("/")[-1]

    if name is not None:
        new_object = '{}/{}-{}.json'.format(prefix, keyNoExt, name)
    else: 
        new_object = '{}/{}.json'.format(prefix, keyNoExt)

    bucket = request["bucketName"]
    fileName = '/tmp/{}-output.json'.format(keyNoExt)

    # save JSON output as a file to be uploaded
    with open(fileName, 'w') as f:
        json.dump(response, f)
        
    print('uploading file: {}\n'.format(new_object))
    s3.upload_file(fileName, bucket, new_object)

def handler(event, context):
    print("event: {}\n".format(event))

    topicArn = os.environ.get('TOPIC_ARN')
    roleArn = os.environ.get('ROLE_ARN')

    request = {}
    request["bucketName"] = event['Records'][0]['s3']['bucket']['name']
    request["objectName"] = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    ext = os.path.splitext(request["objectName"].lower())[1]

    # if the file is JPG and PNG we can make a synchronus call to Textract. If it is a PDF, it have to be asynchronous.     
    if (ext and ext in [".jpg", ".jpeg", ".png"]):
        #TODO: create your sync call here. 
        #use download_object(request) to download the object so you can send it to Textract
        print('sync API call')

        #ANSWER:
        syncResponse = textract.analyze_document(
            Document={
                'S3Object': { 
                    'Bucket': request["bucketName"],
                    'Name': request["objectName"]
                }
            },
            FeatureTypes=[
                'TABLES',
                'FORMS'
            ]
        )

        upload_object(request, syncResponse)
        ###END ANSWER###

    else: 
        #TODO: create your async call here
        # use download_object(request) to download the object so you can send it to Textract
        print('async API call')
        asyncResponse = None 

        #ANSWER:
        # Call the async operation
        asyncResponse = textract.start_document_analysis(
            DocumentLocation={
                'S3Object': {
                    'Bucket': request["bucketName"],
                    'Name': request["objectName"]
                }
            },
            FeatureTypes=[
                    'TABLES',
                    'FORMS'
            ],
            NotificationChannel={
                'SNSTopicArn': topicArn,
                'RoleArn': roleArn 
            },
            ClientRequestToken=str(uuid.uuid4())
        )

        response = textract.get_document_analysis(
            JobId=asyncResponse["JobId"]
        )

        while response["JobStatus"] == 'IN_PROGRESS':
            print('waiting for the textract job to complete')
            time.sleep(10)
            response = textract.get_document_analysis(
                JobId=asyncResponse["JobId"]
            )
        else:
            upload_object(request, response)
        ###END ANSWER###

    # should return 200 for the API Gateway. Body can be different, if required.
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }
