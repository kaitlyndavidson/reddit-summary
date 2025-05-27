# reddit-summary

Small personal project to learn ML & NLP techniques. This repo includes an automated ETL pipeline that uses PRAW to extract Reddit data, cleans text, uses a pre-trained HuggingFace transformer to summarize post and comments content, and stores data locally + uploads data to AWS S3 using boto3. There is also a scikit-learn classification model that is trained and evaluated on Reddit comments sentiment (agree/neutral/disagree). The results are stored in a classification report and confusion matrix.

### Setup
Using python 3.11, create and activate a virtual environment and install dependencies:
```
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a Reddit app:
1. Login at https://www.reddit.com/prefs/apps
2. Create an app
    - Type: script
    - Redirect uri: fill in with anything (ex: `http://localhost:8080`) - won't use this, but can't leave it blank
3. Save the personal use script and secret keys for the next step

Store Reddit credentials as environment variables:
1. Create an environment file (`.env`)
2. Populate the .env with the credentials from the Reddit app:
```
REDDIT_CLIENT_ID="<Reddit personal use script key>"
REDDIT_CLIENT_SECRET="<Reddit secret key>"
REDDIT_USER_AGENT="<platform>:<app ID>:<version string> (by u/<Reddit username>)"
```

Configure AWS credentials:
1. Login at https://console.aws.amazon.com/iam
2. Click Users -> Create user with the following permissions:
    - AmazonS3FullAccess
    - AWSLambda_FullAccess
3. Click on the user -> Security credentials -> Create access key
    - Use case: Local code
4. Save the access key and secret access key for later
5. Install the AWS CLI (instructions for macOS):
    - `curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"`
    - `sudo installer -pkg AWSCLIV2.pkg -target /`
    - `rm AWSCLIV2.pkg`
6. Run `aws configure` and enter credentials
    - Region: us-west-2 (or other)
    - Output format: json
7. Go to https://s3.console.aws.amazon.com/s3
8. Click Create bucket - add name and region, leave everything else as is
9. Add the bucket name and region to the .env:
```
AWS_BUCKET_NAME="<bucket name>"
AWS_REGION="<region>"
```
10. Go to https://console.aws.amazon.com/iam -> Roles -> Create role
11. Click AWS service -> Lambda -> add these permissions:
    - AWSLambdaBasicExecutionRole
    - AmazonS3FullAccess
12. Click on the new role and copy the ARN
13. Add your AWS account number (under profile) and lambda role ARN to the .env:
```
AWS_ROLE_ARN="<arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_EXECUTION_ROLE_ARN>"
```
