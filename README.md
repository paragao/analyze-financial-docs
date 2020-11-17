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
     *Under General Configuration*
     - **Event name**: analysis-using-textract
     - **Prefix**: textract_input/
     *Under Event types*
     - Select the checkbox next to **All object create events**
     *Under Destination*
     - Select **Lambda Function**
     - Select **Choose from your Lambda functions**
     - Chose the lambda function that begins with **textract-analysis-** followed by a hash key 
 8. Follow steps 5 and 6 to create another automation, but this time use the following information:
     *Under General Configuration*
     - **Event name**: analysis-using-comprehend
     - **Prefix**: textract_output/
     *Under Event types*
     - Select the checkbox next to **All object create events**
     *Under Destination*
     - Select **Lambda Function**
     - Select **Choose from your Lambda functions**
     - Chose the lambda function that begins with **comprehend-analysis-** followed by a hash key 

Now that you have created your automation rules, two things will happen:
* whenever a file is created/updated in the *textract_input/* folder then an AWS Lambda function will be called and the new/altered object information will be sent as the event of the funtion. This function will use that information to call the Amazon Textract APIs. The results will be output in the *textract_output/* folder.

* whenever a file is created/updated in the *textract_output/* folder then an AWS Lambda function will be called and the new/altered object information will be sent as the event of the funtion. This function will use that information to call the Amazon Comprehened APIs. The results will be output in the *comprehend_output/* folder. This folder will only be created after the whole processing is complete. 

Excellent! Now you have the foundation for the workflow to work. But if you look in the AWS Lambda functions you will see that there are gaps you will need to fill in. 
![Mr Burns Excellent gif](https://big.assets.huffingtonpost.com/Mr-Burns-Saying-Excellent.gif)

&nbsp;
Let's go ahead and start looking at the beauty of using AI Services to build our application! 

## Step Two - using AI Services to build intelligent applications
The required AWS Lambda functions have already been deployed in your account, with its required IAM Roles. But, those functions are not yet... well, functional :-)

&nbsp;
We will be using two AI Services in our application: [Amazon Textract], which allows us to analyze PDF, PNG, or JPG, files to extract text, tables, and key/value pairs, and Amazon Comprehend, which uses Natural Language Processing to extract insights about the content of documents.