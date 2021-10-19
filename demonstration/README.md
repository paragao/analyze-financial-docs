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

The references for the documentation are in the following links: 
 * Boto3 SDK can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html).
 * Amazon Textract in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html#id6)
 * Amamzon Comprehend in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#id64)
 * Amazon S3 in Boto3 can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)

&nbsp; 
# Before you begin
## Creating the lab environment
There are two scenarios you can follow here: 

 * **a. You are attending an AWS event and an AWS architect has provided you with credentials to an account**
     * If this is your case, you should already been provided with an account, credentials, and the required steps to login to the AWS Console. 
     * You can skip this step and go to Step Two

 * **b. You want to run this code by yourself in your own account**
     * first you need to access you AWS Console. Please login to an account before proceeding.
     * then use [this AWS Cloudformation template](https://github.com/paragaoaws/analyze-financial-docs/blob/main/base-template.yaml) to deploy the solution in your account
     * fill out the required parameters and click "Next" on the other prompts until you can click on "Create Stack" at the end.
     * make sure you allow AWS Cloudformation to create IAM resources in your behalf.

&nbsp;
# The demonstration guide
The following diagram has been deployed in your account: 


![]()


All you need now is to upload files to the textract_input/ prefix and see the magic happening. All outputs will appear in a new prefix called comprehend_output/ . You can use a set of scripts provided to better view the results, or you can develop your own website to better integrate with this solution.


### Testing - uploading a file and looking at the logs
Ok, so now let's test this solution. Upload a file to your bucket inside the **textract_input/** folder. After you have uploaded it, go to the Amazon CloudWatch Logs console and click on **Log Groups** on the left hand side menu. Click on the **Log Stream** that will be shown, and then expand the logs. There are a lot of data there!


If you don't have a file to test with, here are some links you can use:
* [G-20 Surveillance Notes, giving an overview of the global economic](https://www.imf.org/external/np/g20/pdf/2020/071620.pdf)
* [COVID-19 situation update for the EU/EEA and the UK, as of 17 November 2020](https://www.ecdc.europa.eu/en/cases-2019-ncov-eueea)
* [Front page of a Brazilian newspaper focused on Finance](https://www.vercapas.com.br/edicao/capa/valor-economico/2019-12-09/)


As you could see, as you followed the instructions above, it was as easy as call different APIs in the same function in order to extract rich insights from our text. And it was only possible because Amazon Textract had already helped us extracting the text from our scanned documents. 


With that info loaded in an Amazon S3 bucket we can do a lot of different things, such as:
* use AWS Glue to crawl or data and identify the metadata creating tables which we can query using Amazon Athena;
* use AWS Lake Formation to segment and segregate our users access to the specific data they are elligible, increasing security and enforcing governance of the data;
* use Amazon Quicksight to create dashboards based on our data, and use Machine Learning models that will detect anomalies and other rich information;
* customize our solution to use a custom dictionary or custom model and still have the easeness of using AI Services.

&nbsp;
# Conclusion and next steps
We have achieved a lot in this tutorial and it was very easy but very powerfull as well! In a few seconds we had our documents analyzed by Amazon Textract and Amazon Comprehend as well. We were able to extract a lot of insights and now we can keep on using that information to build intelligent applications. Some ideas to use those insights: 
 * reduce churn by understanding your user better;
 * reduce fraud from forms and other documents;
 * create a sentiment heat map of your products;
 * automate document analysis, reducing labor hours required to process documents;
 * enrich your data lake with all the insights extracted from your documents;
 * understand patterns that are not easy to spot, such user segmentation and personalization;
 * desing Next Best Action (NBA) and Next Best Offer (NBO) products, enriching the decision model with more data!

***
Author: Paulo Aragão
