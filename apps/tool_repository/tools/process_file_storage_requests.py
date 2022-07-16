from typing import Dict

from file_storage_utils import upload_file, delete_file


def process_upload_file(file, content_type) -> Dict[str, str]:
    return {"status": upload_file(file, content_type)}


def process_delete_file(delete_file_form) -> Dict[str, str]:
    return {"status": delete_file(delete_file_form["bucket"], delete_file_form["FilePath"])}
