from distutils.command.upload import upload
from typing import Dict

from werkzeug import Response

from file_storage_utils import upload_file, upload_file_object

def process_upload_file_object(file, content_type) -> Dict[str, bool]:
    
    return {"success": upload_file_object(file, content_type)}

def process_upload_file(file_upload_form: Dict[str, str]) -> Dict[str, bool]:
    return {"success": upload_file(file_upload_form["FileName"], file_upload_form["ObjectName"])}