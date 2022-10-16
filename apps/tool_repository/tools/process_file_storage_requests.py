from typing import Dict, List

from file_storage_utils import upload_file, delete_file, list_bucket_files


def process_upload_file(file, content_type) -> Dict[str, str]:
    return {"status": upload_file(file, content_type)}


def process_delete_file(delete_file_form) -> Dict[str, str]:
    return {"status": delete_file(delete_file_form["bucket"], delete_file_form["FilePath"])}


def delete_process_list_bucket_files(list_file_form) -> Dict[Dict, List[str]]:
    return list_bucket_files(list_file_form["bucket"], list_file_form["prefix"])
