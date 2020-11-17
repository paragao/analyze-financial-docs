import json
import boto3
import uuid
import os
import math
import urllib
import sys

s3 = boto3.client('s3')
prefix = 'comprehend_output'

### ADD YOUR COMPREHEND BOTO3 CLIENT HERE:

######

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
    keyNoExt = os.path.splitext(request["objectName"].lower())[0].split("/")[1]

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

    request = {}
    request["bucketName"] = event['Records'][0]['s3']['bucket']['name']
    request["objectName"] = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # initializing specific variables
    text = " "
    entities = {}
    sentiment = {}
    phrases = {}
    syntax = {}

    # download the previous processed file and read it - output from the Textract call
    obj = download_object(request)
    with open(obj, 'r') as json_file:
        tmp = json.load(json_file)
        blocks = tmp["Blocks"]
    
    # extract only the blocks which are a LINE (which contain Text and WORDS within)
    for block in blocks:
        if block["BlockType"] == 'LINE':
            text = text + block["Text"] + " "

    text = text.strip()

    #### STEP 1 - LANGUAGE DETECTION ####

    ### LANGUAGE - ANSWER HERE:


    ###
    
    language = response["Languages"][0]["LanguageCode"]
    print('Language detected: {}'.format(language))

    upload_object(request, response, 'language')

    #### STEP 2 - ENTITIES DETECTION ####

        ### ENTITIES - ANSWER HERE:


        ###
    
    print('Entities detected: {}'.format(entities))
    upload_object(request, entities, 'entities')

    #### STEP 3 - SENTIMENT DETECTION ####

        ### SENTIMENT - ANSWER HERE:


        ###
    
    print('Sentiment detected: {}'.format(sentiment))
    upload_object(request, sentiment, 'sentiment')

    #### STEP 4 - KEY PHRASES DETECTION ####

        ### KEY_PHRASES - ANSWER HERE:


        ###
    
    print('Key phrases detected: {}'.format(phrases))
    upload_object(request, phrases, 'key_phrases')

    #### STEP 5 - SYNTAX DETECTION ####


        ###
    
    print('Syntax detected: {}'.format(syntax))
    upload_object(request, syntax, 'syntax')

    # ideally return 200 always and since the function send erros to logs
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }