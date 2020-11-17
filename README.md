# analyze-financial-docs
Solution using Amazon Textract, Amazon Eventbridge, and other tools to extract data from financial documents and analyze it

# Pre-requisites
In order to be able to run this workshop you will need:
 * be familiar with AWS and its services, specially AWS Lambda, AWS Cloudformation, Amazon API Gateway, and Amazon S3;
 * be familiar with Python programming and SDK's. We are not asking that you be an expert with lots of experience, just that you might have already worked on a small function or script and understand the basics of Python;
 * be familiar with SDK documentation. We will be using the [Boto3 SDK](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) and understanding how to read a SDK documentation is key to allow you to complete the steps below without looking at the spoilers.

&nbsp;
Bear in mind that you don't need to know anything about Machine Learning modeling or specific frameworks. This workshop will use AI Services, which provides API endpoints that you can use to consume ML models that have been trained on a curated dataset and do work well in most situations.

&nbsp; 
The documentation references are in the following links: 
 * Boto3 SDK can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
 * Amazon Textract in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#id6)
 * Amamzon Comprehend in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#id64)
 * Amazon S3 in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

&nbsp; 
# Before you begin
## Create the lab environment
There are two scenarios you can follow here: 

 **a. You are attending an AWS event and an AWS architect has provided you with credentials to an account**
     * If this is your case, you should already been provided with an account, credentials, and the required steps to login to the AWS Console. 
     * You can skip this step and go to Step Two

 **b. You want to run this code by yourself in your own account**
  * first you need to access you AWS Console. Please login to an account before proceeding.
  * then use [this AWS Cloudformation template](https://github.com/paragaoaws/analyze-financial-docs/blob/main/base-template.yaml) to deploy the solution in your account
  * fill out the required parameters and click "Next" on the other prompts until you can click on "Create Stack" at the end.
  * make sure you allow AWS Cloudformation to create IAM resources in your behalf.

&nbsp;
# The workshop guide
The following diagram has been deployed in your account: 
![]()

&nbsp; 
Although this might seem a complete diagram, there are parts that are missing in order for the solution to run. Now we need to follow the steps below in order to complete it:

&nbsp;
## Step One - configure the automation using Amazon S3 Event Notifications
First we need to create prefixes which will be used to upload the files and store the results: 

 1. Go to the AWS CloudFormation console and select the stack deployed for this workshop. In the Output tab you will find the name of the bucket created for those files.
 2. Now go to the Amazon S3 console and navigate to your bucket. Click on its name. 
 3. Create two folders named as such: 
     - textract_input
     - textract_output

&nbsp;
Now that we have a place to upload our files and store the model results, let's make so that whenever a new file is uploaded to the *textract_input/* prefix a function is automatically called to start the document analysis. In order to do that, complete the following steps: 

 4. On the Amazon S3 console, inside your bucket, click on the **Properties** tab.
 5. Scroll down until you find **Event notifications**
 6. Click on **Create event notification**
 7. You will be creating two events. Follow the input information below for the first one:
     - *Under General Configuration*
         - **Event name**: analysis-using-textract
         - **Prefix**: textract_input/
     - *Under Event types*
         - Select the checkbox next to **All object create events**
     - *Under Destination*
         - Select **Lambda Function**
         - Select **Choose from your Lambda functions**
         - Chose the lambda function that begins with **textract-analysis-** followed by a hash key 
 8. Follow steps 5 and 6 to create another automation, but this time use the following information:
     - *Under General Configuration*
         - **Event name**: analysis-using-comprehend
         - **Prefix**: textract_output/
     - *Under Event types*
         - Select the checkbox next to **All object create events**
     - *Under Destination*
         - Select **Lambda Function**
         - Select **Choose from your Lambda functions**
         - Chose the lambda function that begins with **comprehend-analysis-** followed by a hash key 

Now that you have created your automation rules, two things will happen:
* whenever a file is created/updated in the *textract_input/* folder then an AWS Lambda function will be called and the new/altered object information will be sent as the event of the funtion. This function will use that information to call the Amazon Textract APIs. The results will be output in the *textract_output/* folder.

* whenever a file is created/updated in the *textract_output/* folder then an AWS Lambda function will be called and the new/altered object information will be sent as the event of the funtion. This function will use that information to call the Amazon Comprehened APIs. The results will be output in the *comprehend_output/* folder. This folder will only be created after the whole processing is complete. 

The foundation has been setup for your intelligent application. Excellent! 
![Mr Burns Excellent gif](https://big.assets.huffingtonpost.com/Mr-Burns-Saying-Excellent.gif)


But if you look in the AWS Lambda functions you will see that there are gaps you will need to fill in. Let's go ahead and start looking at the beauty of using AI Services to build our application! 

&nbsp;
## Step Two - using AI Services to build intelligent applications
The required AWS Lambda functions have already been deployed in your account, with its required IAM Roles. But, those functions are not yet... well, functional :-)

&nbsp;
We will be using two AI Services in our application: [Amazon Textract], which allows us to analyze PDF, PNG, or JPG, files to extract text, tables, and key/value pairs, and Amazon Comprehend, which uses Natural Language Processing to extract insights about the content of documents.

&nbsp;
### Amazon Textract - text detection and analysis
The Amazon Textract AI service has a few APIs you can use. 

What we will do here is use two APIs: one that calls the service in a synchronous fashion, and the other one asynchronously. Let's see how we can send a document to be analyzed by Amazon Textract:

 1. First we need to make sure we are importing the boto3 library and creating a boto3.client to connect to the service
 ```
 import boto3

 textract = boto3.client('textract')
 ```
 2. Then we need to call the Amazon Textract API [AnalyzeDocument](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.analyze_document) and upload the object to the *textract_output/* folder.
 ```
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
 ```

Ok, so let's dive deeper into what we have done here. The AnalyzeDocument API requires some information, such as the source bucket where your file is, the name of the object, and if you want to analyze more than just text. Our function is already provisioned with some helper functions (which I will not go into detail here). So we are getting the object name and the source bucket from the event that was sent to the function (you can check the logs to see the complete payload, if you want), then we are calling *textract.analyze_document()* and configuring it to not only capture the text in the document, but also capture any forms or tables that the document have. This allows Amazon Textract to create relationships between those elements, and present those relationships in the output JSON file. Right at the end, after the API has returned, we upload the results into the *textract_output/* folder. This will trigger another of our automation but... more on that later!

&nbsp;

Go ahead, and copy and paste that code into your AWS Lambda function. You should paste it right after the **\#\# ANALYZE_DOCUMENT ANSWER: ** comment. Make sure it is properly idented as we don't want to bump into runtime errors.

&nbsp;

But there is a caveat! The AnalyzeDocument API, although very good whenever you need a synchronous response, does not process PDF files only PNG and JPEG. In order to process PDF files as well, we need to call the [StartDocumentAnalysis](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#Textract.Client.start_document_analysis) API. Let's see how we can achieve that:
 3. Add the following lines to your Lambda function right after the comment **\#\# START_DOCUMENT_ANALYSIS ANSWER: **
 ```
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
 ```

When calling the StartDocumentAnalysis API we need to provide additional information to the service, such as the source bucket and the object name, what features we want to extract form the text, an Amazon SNS Topic ARN (Amazon Resource Name) which will be used to control wether the job has succeeded or not, and an IAM Role ARN allowing Amazon Textract to publish a message into this topic. The last parameter, ClientRequestToken, allows you to re-trigger a specific job (if you send the same token) or make sure that your not accidentally starting the same job over and over again. Since this is an asynchronous call, we need to monitor if the job has completed or not. In order to do that we will use a loop anf call GetDocumentAnalysis using the JobID returned by our StartDocumentAnalysis API call. When the job completes, we use a helper function to upload the object into the *textract_output/* folder. Which, as I mentioned earlier, will trigger the second part of our automation. Let's talk about it now!

&nbsp;
### Amazon Comprehend - Natural Language Processing to extract insights from documents