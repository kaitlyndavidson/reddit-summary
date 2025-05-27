import boto3
import zipfile
import os
from dotenv import load_dotenv

 # TODO: didn't finish setting this up
 
load_dotenv()
LAMBDA_FUNCTION_NAME = "redditSummarizerLambda"
ROLE_ARN = os.getenv('AWS_ROLE_ARN')
RUNTIME = "python3.11"
HANDLER = "lambda_function.lambda_handler"
ZIP_FILE_NAME = "lambda_function.zip"
SOURCE_FILE = "lambda_function.py"
REGION = os.getenv('AWS_REGION')

# zip the lambda function
def zip_lambda():
    with zipfile.ZipFile(ZIP_FILE_NAME, 'w') as zipf:
        zipf.write(SOURCE_FILE)

# deploy lambda to AWS
def deploy_lambda():
    client = boto3.client('lambda', region_name=REGION)
    # read the zipped file
    with open(ZIP_FILE_NAME, 'rb') as f:
        zipped_code = f.read()
    # create and publish the lambda function
    try:
        response = client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime=RUNTIME,
            Role=ROLE_ARN,
            Handler=HANDLER,
            Code=dict(ZipFile=zipped_code),
            Timeout=60, # seconds
            MemorySize=128,
            Publish=True
        )
    # if the lambda already exists, update it instead of creating it
    except client.exceptions.ResourceConflictException:
        response = client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ZipFile=zipped_code,
            Publish=True
        )
