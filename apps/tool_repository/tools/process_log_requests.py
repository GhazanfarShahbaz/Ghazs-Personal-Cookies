from log_utils import split_up_log_file
from typing import Dict, List

def process_get_logs() -> Dict[str, List[str]]:
    return split_up_log_file()