import boto3

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url='http://localhost:8000',
        aws_access_key_id='test_access',
        aws_secret_access_key='test_secret'
    )

def create_bucket(bucket_name):
    s3_client = get_s3_client()
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except s3_client.exceptions.BucketAlreadyExists:
        print(f"Bucket '{bucket_name}' already exists.")
    except Exception as e:
        print(f"Failed to create bucket: {e}")

def upload_image_to_s3(bucket_name, image_name, image_data):
    s3_client = get_s3_client()
    s3_client.upload_fileobj(image_data, bucket_name, image_name)

def download_image_from_s3(bucket_name, image_name):
    s3_client = get_s3_client()
    obj = s3_client.get_object(Bucket=bucket_name, Key=image_name)
    return obj['Body'].read()
