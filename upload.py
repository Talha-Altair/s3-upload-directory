import os
from sys import argv
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.client import ClientError
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
# Function to upload to s3
def upload_to_aws(bucket, local_file, s3_file):
    """local_file, s3_file can be paths"""
    
    print('  Uploading ' +local_file + ' as ' + bucket + '/' +s3_file)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print('  '+s3_file + ": Upload Successful")
        print('  ---------')
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

def upload_folder(LOCAL_FOLDER_PATH,BUCKET_NAME,S3_FOLDER_NAME):

    bucket_name = BUCKET_NAME

    local_folder  = LOCAL_FOLDER_PATH

    s3_folder = S3_FOLDER_NAME

    walks = os.walk(local_folder)

    """For file names"""
    for source, dirs, files in walks:
        print('Directory: ' + source)
        for filename in files:
            # construct the full local path
            local_file = os.path.join(source, filename)
            # construct the full Dropbox path
            relative_path = os.path.relpath(local_file, local_folder)
            s3_file = os.path.join(s3_folder, relative_path)
            upload_to_aws(bucket_name, local_file, s3_file)

if __name__ == '__main__':

    upload_folder( LOCAL_FOLDER_PATH="./test-folder",
                   BUCKET_NAME='tact-tester-29',
                   S3_FOLDER_NAME="chumma")