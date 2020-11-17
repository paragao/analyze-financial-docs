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
    langText = text
    
    if sys.getsizeof(langText) > 5000: 
        langText = text[:3000]

    ### LANGUAGE - ANSWER HERE:


    ###
    
    language = response["Languages"][0]["LanguageCode"]
    print('Language detected: {}'.format(language))

    upload_object(request, response, 'language')

    #### STEP 2 - ENTITIES DETECTION ####
    entitiesText = text

    if sys.getsizeof(entitiesText) > 5000:
        loops = math.ceil(sys.getsizeof(entitiesText) / 5000)
        while loops > 0:
            if len(entitiesText) < 4000:
                size = len(entitiesText)
            else:
                size = 4000

            entities[loops] = comprehend.detect_entities(
                Text=entitiesText[:size],
                LanguageCode=language
            )
            entitiesText = entitiesText[size:]
            loops -= 1
    else: 
        ### ENTITIES - ANSWER HERE:


        ###
    
    print('Entities detected: {}'.format(entities))
    upload_object(request, entities, 'entities')

    #### STEP 3 - SENTIMENT DETECTION ####
    sentimentText = text
    
    if sys.getsizeof(sentimentText) > 5000:
        loops = math.ceil(sys.getsizeof(sentimentText) / 5000)
        while loops > 0:
            if len(sentimentText) < 4000:
                size = len(sentimentText)
            else:
                size = 4000

            sentiment[loops] = comprehend.detect_sentiment(
                Text=sentimentText[:size],
                LanguageCode=language
            )
            sentimentText = sentimentText[size:]
            loops -= 1            
    else:
        ### SENTIMENT - ANSWER HERE:


        ###
    
    print('Sentiment detected: {}'.format(sentiment))
    upload_object(request, sentiment, 'sentiment')

    #### STEP 4 - KEY PHRASES DETECTION ####
    phrasesText = text
    
    if sys.getsizeof(phrasesText) > 5000:
        loops = math.ceil(sys.getsizeof(phrasesText) / 5000)
        while loops > 0:
            if len(phrasesText) < 4000:
                size = len(phrasesText)
            else:
                size = 4000

            phrases[loops] = comprehend.detect_key_phrases(
                Text=phrasesText[:size],
                LanguageCode=language
            )
            phrasesText = phrasesText[size:]
            loops -= 1
    else:
        ### KEY_PHRASES - ANSWER HERE:


        ###
    
    print('Key phrases detected: {}'.format(phrases))
    upload_object(request, phrases, 'key_phrases')

    #### STEP 5 - SYNTAX DETECTION ####
    syntaxText = text
    
    if sys.getsizeof(syntaxText) > 5000:
        loops = math.ceil(sys.getsizeof(syntaxText) / 5000)
        while loops > 0:
            if len(syntaxText) < 4000:
                size = len(syntaxText)
            else:
                size = 4000

            syntax[loops] = comprehend.detect_syntax(
                Text=syntaxText[:size],
                LanguageCode=language
            )
            syntaxText = syntaxText[size:]
            loops -= 1
    else:
        ### SYNTAX - ANSWER HERE:


        ###
    
    print('Syntax detected: {}'.format(syntax))
    upload_object(request, syntax, 'syntax')

    # ideally return 200 always and since the function send erros to logs
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }