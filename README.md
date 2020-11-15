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
# Major steps
## Step One - deploy the template and access your account
There are two scenarios you can follow here: 

 **a. You are attending an AWS event and an AWS architect has provided you with credentials to an account**
  * If this is your case, you should already been provided with an account, credentials, and the required steps to login to the AWS Console. 
  * You can skip this step and go to Step Two

 **b. You want to run this code by yourself in your own account**
  * first you need to access you AWS Console. Please login to an account before proceeding.
  * then use [this AWS Cloudformation template](https://) to deploy the solution in your account
  * fill out the required parameters and click "Next" on the other prompts until you can click on "Create Stack" at the end.
  * make sure you allow AWS Cloudformation to create IAM resources in your behalf.

&nbsp;
## Step Two - create a function that will get documents from an Amazon S3 bucket and process them
Part of the template deployment was that it has created some helper functions for you, such as a function that will upload/download data from Amazon S3 and provide you with some variables. If you want, go ahead and take a look at them. They have been created as part of your AWS Lambda function. The name of the bucket and other parameters you have filled out during the template creation were used as ENVIROMENT VARIABLES in AWS Lambda. You can verify them using the AWS Console.


&nbsp;
If you go to the AWS Lambda console you will see the funcion the template have deployed. The code is partially written for you and the objective of this step is to write additional code that you need to use Amazon Textract. Those are the major steps you need to complete to finish sucesfully this step:
 1. Create a logic that will download an object from Amazon S3 whenever some new file has been uploaded to the *input/* prefix. Use the helper functions to do that;
 2. Create a logic that will trigger an Amazon Textract API Sync call to process the document and store its output back in your bucket, but in a different prefix. 

&nbsp; 
The documentation for the pieces you need to complet this steps are in the following links: 
 * Boto3 SDK can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
 * Amazon Textract in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#id6)
 * Amazon S3 in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

&nbsp; 
## Step Three - create a function that will analyze the extracted text from the document
The template also deployed an addition AWS Lambda fucntion. As in Step Two, this function is partially written and there are some helper functions. In order to complete this step sucesfully you have to:
 1. Create a logic that will download an object from Amazon S3 whenever some new file has been uploaded to the *textract_processed/* prefix. Use the helper functions to do that;
 2. Create a logic that will trigger an Amazon Comprehend API call to process the new document and store its output back in your bucket, but in a different prefix.

&nbsp;
## Step Four - create a set of API to be used in an application
Although you can use direct API calls to the public AWS services endpoints, it is a best practice to have an API gateway solution which your applications can consume your APIs. This will allow you to decouple the backend and the frontend.

To complete this step sucesfully you will need to:
 1. Create a set of APIs using Amazon API Gateway and connect them with your AWS Lambda fucntions;
 2. Create a new AWS Lambda function that will put 