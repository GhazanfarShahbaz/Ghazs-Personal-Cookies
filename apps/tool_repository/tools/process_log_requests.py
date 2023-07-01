from log_utils import split_up_log_file
from typing import Dict, List


def process_get_logs() -> Dict[str, List[str]]:
    """
    Processes a request to retrieve log files.

    This function calls the `split_up_log_file` function to retrieve log files and returns them as a dictionary containing the
    file names and their contents.

    Returns:
        A dictionary containing the file names and their contents as a list of strings.
    """

    return split_up_log_file()
