from datetime import datetime
from typing import Dict, List

PATH_TO_LOG_FILE: str = "/home/ghaz/flask_gateway/logs/"


def split_up_log_file() -> Dict[str, List[str]]:
    """
    Splits up a log file by application.

    This function reads a log file from `PATH_TO_LOG_FILE` and splits it up into separate lists of log entries by application.
    The log entries are identified as belonging to a particular application by the path to the log file contained in the entry.
    The function returns a dictionary with application names as keys and lists of log entries as values.

    Returns:
        A dictionary with application names as keys and lists of log entries as values.
    """

    # current_log_file: str = '{:%Y-%m-%d}.log'.format(datetime.now())

    log_file = open(f"{PATH_TO_LOG_FILE}app.log", "r")

    log_dictionary: Dict[str, List[str]] = {"personal_website": []}
    previous_app: str = "personal_website"

    for line in log_file:
        split_colon: List[str] = line.split("|")

        app: str = previous_app

        if len(split_colon) >= 2:
            path_to_file: str = split_colon[1]

            # TODO: Replace this so we don't use if statements
            if "tool_repository" in path_to_file:
                app = "tools"
            elif "knowledge_graph" in path_to_file:
                app = "knowledge_graph"
            elif "personal_webnsite" in path_to_file:
                app = "personal_website"

            if not app in log_dictionary:
                log_dictionary[app] = []

            previous_app = app

        log_dictionary[app].append(line)

    return log_dictionary
