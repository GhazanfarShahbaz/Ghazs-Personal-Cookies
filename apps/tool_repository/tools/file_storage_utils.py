"""
file_name = file_storage_utils.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used for storing and retrieving files from s3 buckets. 
Edit Log:
07/09/2023
-   Conformed to pylint conventions.
"""

from os import environ
from typing import Dict, List

import boto3

FUNCTION_MAPPER: Dict[str, callable] = {
    "client": boto3.client,
    "resource": boto3.resource,
}


def get_aws_credentials() -> Dict[str, str]:
    """
    Gets the AWS credentials from environment variables and returns them as a dictionary.

    This function extracts the AWS credentials from the following environment variables:
        - AWS_FILE_SERVICE
        - AWS_ACCESS_KEY_ID
        - AWS_ACCESS_KEY
        - AWS_PASSWORD
        - AWS_REGION_NAME

    Returns:
        A dictionary containing the AWS credentials.
    """

    return {
        "AWS_FILE_SERVICE": environ["AWS_FILE_SERVICE"],
        "AWS_ACCESS_KEY_ID": environ["AWS_ACCESS_KEY_ID"],
        "AWS_ACCESS_KEY": environ["AWS_ACCESS_KEY"],
        "AWS_PASSWORD": environ["AWS_PASSWORD"],
        "AWS_REGION_NAME": environ["AWS_REGION_NAME"],
    }


def get_aws_client_or_resource(aws_type: str) -> any:
    """
    Creates a boto3 client or resource for the specified AWS type.

    This function takes an AWS type (either "client" or "resource") as
    input and uses it to create either a boto3 client or resource object.
    It uses the AWS credentials stored in environment variables to create the
    client/resource object.

    Args:
        aws_type: A string representing the type of AWS object to create
                  ("client" or "resource").

    Returns:
        A boto3 client or resource object for the specified AWS type.

    Raises:
        KeyError: If the supplied aws_type is not a valid key in the
                  FUNCTION_MAPPER dictionary.
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
    Uploads a file to an AWS S3 bucket.

    This function takes a file and a content type as input, and uploads the file to
    an AWS S3 bucket using the boto3 client associated with the AWS environment variables.

    Args:
        file: The file to be uploaded.
        content_type: The content type of the file.

    Returns:
        A string representing the success or failure of the upload process.

    """

    client = get_aws_client_or_resource("client")
    bucket_name: str = environ["AWS_BUCKET_NAME"]

    try:
        client.put_object(
            Body=file,
            Bucket=bucket_name,
            Key=f"server_files/{file.filename}",
            ContentType=content_type,
        )
    except:  # pylint: disable=bare-except
        return "Failed to upload file"
    finally:
        file.close()

    return "success"


def delete_file(bucket_name: str, file_path: str) -> str:
    """
    Deletes a file from an AWS S3 bucket.

    This function takes a bucket name and a file path as input, and deletes the specified
    file from the AWS S3 bucket using the boto3 client associated with the AWS environment
    variables.

    Args:
        bucket_name: The name of the AWS S3 bucket containing the file to be deleted.
        file_path: The file path of the file to be deleted.

    Returns:
        A string representing the success or failure of the file deletion process.
    """

    client = get_aws_client_or_resource("client")

    client.delete_object(Bucket=bucket_name, Key=file_path)

    return "Success"


def list_bucket_files(bucket_name: str, prefix: str) -> Dict[Dict, List[str]]:
    """
    Lists files in an AWS S3 bucket with an optional prefix.

    This function takes the name of an AWS S3 bucket and an optional prefix as input, and
    returns a dictionary with two keys: "files" and "folders". The "files" key contains a
    list of all the files in the bucket with the specified prefix, while the "folders" key
    contains a list of all the folders (directories) in the bucket with the specified prefix.

    Args:
        bucket_name: The name of the AWS S3 bucket.
        prefix: An optional prefix used to filter the files/folders in the bucket.

    Returns:
        A dictionary with two keys: "files" and "folders". The "files" key contains a
        list of all the files in the bucket with the specified prefix, while the "folders"
        key contains a list of all the folders in the bucket with the specified prefix.
    """

    client = get_aws_client_or_resource("resource")
    bucket = client.Bucket(bucket_name)
    prefix = prefix.strip()

    bucket_data: list = (
        bucket.objects.all() if not prefix else bucket.objects.filter(Prefix=prefix)
    )

    data: Dict[Dict, List[str]] = {"files": [], "folders": []}

    for file in bucket_data:
        bucket_entry_name: str = file.key
        entry_type: str = "files" if not bucket_entry_name.endswith("/") else "folders"

        data[entry_type].append(file.key)

    return data
