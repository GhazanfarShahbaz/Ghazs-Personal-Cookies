"""
file_name = log_utils.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to handle log files.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
-   Fixed personal_website bug
"""

from typing import Dict, List

PATH_TO_LOG_FILE: str = "/home/ghaz/flask_gateway/logs/"


def split_up_log_file() -> Dict[str, List[str]]:
    """
    Splits up a log file by application.

    This function reads a log file from `PATH_TO_LOG_FILE` and splits it up into separate
    lists of log entries by application.
    The log entries are identified as belonging to a particular application by the path to
    the log file contained in the entry.
    The function returns a dictionary with application names as keys and lists of log entries
    as values.

    Returns:
        A dictionary with application names as keys and lists of log entries as values.
    """

    # current_log_file: str = '{:%Y-%m-%d}.log'.format(datetime.now())
    log_dictionary: Dict[str, List[str]] = {"personal_website": []}
    apps: Dict[str, str] = {
        "personal_website": "personal_website",
        "tool_repository": "tools",
        "knowledge_graph": "knowledge_graph",
        "coding_questions": "coding_qustions"
    }

    with open(f"{PATH_TO_LOG_FILE}app.log", "r", encoding="utf8") as log_file:
        previous_app: str = "personal_website"

        for line in log_file:
            split_colon: List[str] = line.split("|")

            app: str = previous_app

            if len(split_colon) >= 2:
                path_to_file: str = split_colon[1]
                
                for app_path, app_name in apps.items():
                    if app_path in path_to_file:
                        app = app_name 
                        break

                if not app in log_dictionary:
                    log_dictionary[app] = []

                previous_app = app

            log_dictionary[app].append(line)

    return log_dictionary
