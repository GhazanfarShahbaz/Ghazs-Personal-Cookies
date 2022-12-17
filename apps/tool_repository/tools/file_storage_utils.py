import boto3

from os import environ
from typing import Dict, List

FUNCTION_MAPPER: Dict[str, callable] = {
    "client": boto3.client,
    "resource": boto3.resource
}


def get_aws_credentials() -> Dict[str, str]:
    """
    Returns: 
        Dict[str, str]: Creates a dictionary of aws credentials 
    """
    
    return {
        "AWS_FILE_SERVICE":  environ["AWS_FILE_SERVICE"],
        "AWS_ACCESS_KEY_ID": environ["AWS_ACCESS_KEY_ID"],
        "AWS_ACCESS_KEY": environ["AWS_ACCESS_KEY"],
        "AWS_PASSWORD": environ["AWS_PASSWORD"],
        "AWS_REGION_NAME": environ["AWS_REGION_NAME"],
    }


def get_aws_client_or_resource(aws_type: str) -> any:
    """
    Creates an aws client or resource

    Returns:
        any: A boto3 client or resource
    """
    
    
    credentials: Dict[str, str] = get_aws_credentials()

    client_or_resource = FUNCTION_MAPPER[aws_type](
        credentials["AWS_FILE_SERVICE"],
        aws_access_key_id=credentials["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=credentials["AWS_ACCESS_KEY"],
        region_name=credentials["AWS_REGION_NAME"],
    )

    return client_or_resource


def upload_file(file, content_type) -> str:
    """
        Uploads a file to aws OP_NO_SSLv3
        
        Returns:
            str: A string representing success or fail
    """
    
    client = get_aws_client_or_resource("client")
    bucket_name: str = environ["AWS_BUCKET_NAME"]

    try:
        client.put_object(
            Body=file,
            Bucket=bucket_name,
            Key=f"server_files/{file.filename}",
            ContentType=content_type
        )
    except:
        return "failed to upload file"

    return "success"


def delete_file(bucket_name: str, file_path: str) -> str:
    """
    Deletes a file from s3 given the bucket name and file path
    
    Returns:
        str: A string representing success or fail
    """
    
    client = get_aws_client_or_resource("client")

    client.delete_object(
        Bucket=bucket_name,
        Key=file_path
    )

    return "Success"


def list_bucket_files(bucket_name: str, prefix: str) -> Dict[Dict, List[str]]:
    """
    Lists files in a bucket given an optional prefix
    
    Returns:
        Dict[Dict, List[str]]: Creates a dict which contains a list of files
    """
    
    client = get_aws_client_or_resource("resource")
    bucket = client.Bucket(bucket_name)
    prefix = prefix.strip()

    bucket_data: list = bucket.objects.all(
    ) if not prefix else bucket.objects.filter(Prefix=prefix)

    data: Dict[Dict, List[str]] = {
        "files": [],
        "folders": []
    }

    for file in bucket_data:
        bucket_entry_name: str = file.key
        entry_type: str = "files" if not bucket_entry_name.endswith(
            "/") else "folders"

        data[entry_type].append(file.key)

    return data
