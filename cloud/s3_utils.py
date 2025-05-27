import boto3

# upload json files to S3 - AWS cloud storage service
def upload_to_s3(local_file, bucket, s3_path):
    s3 = boto3.client('s3')
    s3.upload_file(local_file, bucket, s3_path)

# download json files from S3
def download_from_s3(bucket, s3_path, local_file):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3_path, local_file)
