import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Create an S3 client


# Upload a file
def s3_upload_file(file_name, bucket_name, s3_file_name):
    print(f"Attempting to upload {file_name} to {bucket_name} as {s3_file_name}")
    s3 = boto3.client('s3')

    try:
        print("Uploading file...")
        s3.upload_file(file_name, bucket_name, s3_file_name)
        print(f'{file_name} has been uploaded to {bucket_name} as {s3_file_name}')
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except ClientError as e:
        print(f"An error occurred: {e}")

# Download a file
def s3_download_file(file_name, bucket_name, s3_file_name):
    s3 = boto3.client('s3')
    try:
        s3_response = s3.get_object(Bucket=bucket_name, Key=file_name)
        print(f'{s3_file_name} has been downloaded from {bucket_name} to {file_name}')
        # Read the file content
        file_content = s3_response['Body'].read()
        return file_content
    
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except PartialCredentialsError:
        print("Incomplete credentials provided")
    except ClientError as e:
        print(f"An error occurred: {e}")
