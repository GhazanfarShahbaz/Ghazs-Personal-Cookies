"""
file_name = process_file_storage_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to process file storage requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

from typing import Dict, List

from apps.tool_repository.tools.file_storage_utils import (
    upload_file,
    delete_file,
    list_bucket_files,
)


def process_upload_file(file, content_type) -> Dict[str, str]:
    """
    Process a file upload request.

    This function takes a file and a content type and uploads the file to a storage system.
    Then, it returns a dictionary containing the upload status.

    Args:
        file: The file to be uploaded.
        content_type: The MIME type of the file being uploaded.

    Returns:
        A dictionary containing the upload status.
    """

    return {"status": upload_file(file, content_type)}


def process_delete_file(delete_file_form) -> Dict[str, str]:
    """
    Process a file deletion request.

    This function takes a dictionary `delete_file_form` representing the delete
    parameters for a file.
    The function then calls the `delete_file()` method with these parameters to
    delete the file from a storage system.

    Args:
        delete_file_form: A dictionary containing the bucket and file path of the
        file to be deleted.

    Returns:
        A dictionary containing the deletion status.
    """

    return {
        "status": delete_file(delete_file_form["bucket"], delete_file_form["FilePath"])
    }


def delete_process_list_bucket_files(list_file_form) -> Dict[Dict, List[str]]:
    """
    List the files in a bucket.

    This function takes a string `bucket` and an optional string `prefix` and returns a
    dictionary containing the files in the specified bucket.
    If a prefix is provided, only files matching the prefix will be included.

    Args:
        bucket: The name of the bucket to list files from.
        prefix: An optional prefix to filter files by.

    Returns:
        A dictionary containing the files in the specified bucket.
    """

    return list_bucket_files(list_file_form["bucket"], list_file_form["prefix"])
