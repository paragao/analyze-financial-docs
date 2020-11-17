import json
import boto3
import uuid
import os
import math
import urllib
import sys

comprehend = boto3.client('comprehend')
s3 = boto3.client('s3')
prefix = 'comprehend_output'

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
    entities = { }

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

    # step 1: get the document language
        # tip#1: the other comprehend calls required you to define what is the language of the document
    textEncoded = text.encode('utf-8')
    if sys.getsizeof(textEncoded) > 5000: 
        langText = text[:3000]
    else: 
        langText = text

    response = comprehend.detect_dominant_language(
        Text=langText
    )
    
    language = response["Languages"][0]["LanguageCode"]
    print('Language detected: {}'.format(language))

    upload_object(request, response, 'language')

    # step 2: find entities
        # tip#1: detect_entities only support up to 5000 bytes per call. Encode in utf-8 and calculate the size before sending.
    if sys.getsizeof(text) > 5000:
        loops = math.ceil(sys.getsizeof(text) / 5000)
        while loops > 0:
            entities[loop] = comprehend.detect_entities(
                Text=text.strip()[:4000],
                LanguageCode=language
            )
            text = text[4000:]
            loops -= 1
    else: 
        entities = comprehend.detect_entities(
                Text=text,
                LanguageCode=language
            )
    
    print('Entities detected: {}'.format(entities))
    upload_object(request, entities, 'entities')

    # step 3: find the overall sentiment (tone) of the text
        # tip#1: 
    response = comprehend.detect_sentiment(
        Text=text,
        LanguageCode=language
    )
    print('Sentiment detected: {}'.format(response))
    upload_object(request, response, 'sentiment')

    # step 4: detect the key phrases in the text
    response = comprehend.detect_key_phrases(
        Text=text,
        LanguageCode=language 
    )
    print('Key phrases detected: {}'.format(response))
    upload_object(request, response, 'key_phrases')

    ## step 5: find PII entities    
    #    # tip#1: different from Types are found such as BANK_ACCOUNT_NUMBER, BANK_ROUTING, CREDIT_DEBIT_NUMBER
    #    # tip#2: it is only working as an async call start_pii_entities_detection_job()
    #s3UriInput = 's3://{}/{}'.format(request["bucketName"], request["objectName"])
    #s3UriOutput = 's3://{}/comprehend_output/{}-pii-entities.json'.format(request["bucketName"], os.path.splitext(request["objectName"])[0])
    #dataRoleArn = os.environ.get('DATA_ROLE_ARN')
    #
    #response = comprehend.start_pii_entities_detection_job(
    #    InputDataConfig={
    #        'S3Uri': s3UriInput
    #    },
    #    OutputDataConfig={
    #        'S3Uri': s3UriOutput
    #    },
    #    Mode='ONLY_REDACTION', # other mode=ONLY_OFFSETS
    #    RedactionConfig={
    #        'PiiEntityTypes': [
    #            'BANK_ACCOUNT_NUMBER',
    #            'BANK_ROUTING',
    #            'CREDIT_DEBIT_NUMBER',
    #            'CREDIT_DEBIT_CVV',
    #            'CREDIT_DEBIT_EXPIRY',
    #            'PIN',
    #            'EMAIL',
    #            'ADDRESS',
    #            'NAME',
    #            'PHONE',
    #            'SSN',
    #            'DATE_TIME',
    #            'PASSPORT_NUMBER',
    #            'DRIVER_ID',
    #            'URL',
    #            'AGE',
    #            'USERNAME',
    #            'PASSWORD',
    #            'AWS_ACCESS_KEY',
    #            'AWS_SECRET_KEY',
    #            'IP_ADDRESS',
    #            'MAC_ADDRESS' # or it would be easier to type just 'ALL' if you wanted everything
    #        ],
    #        'MaskMode': 'MASK', # or REPLACE_WITH_PII_ENTITY_TYPE
    #        'MaskCharacter': '*'
    #    },
    #    DataAccessRoleArn=dataRoleArn,
    #    LanguageCode=language,
    #    ClientRequestToken=uuid.uuid4()
    #)
    #
    #print('PII entities detection start. Job ID: {}'.format(response))

    # ideally return 200 always and since the function send erros to logs
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }