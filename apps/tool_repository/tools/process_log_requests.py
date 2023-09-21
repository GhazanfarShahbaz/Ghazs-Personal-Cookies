"""
file_name = process_log_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to process log requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

from typing import Dict, List

from apps.tool_repository.tools.log_utils import split_up_log_file


def process_get_logs() -> Dict[str, List[str]]:
    """
    Processes a request to retrieve log files.

    This function calls the `split_up_log_file` function to retrieve log files and returns
    them as a dictionary containing the file names and their contents.

    Returns:
        A dictionary containing the file names and their contents as a list of strings.
    """

    return split_up_log_file()
