from typing import Dict, List
from datetime import datetime

PATH_TO_LOG_FILE: str = "/home/ghaz/flask_gateway/logs/"


def split_up_log_file() -> Dict[str, List[str]]:
    # current_log_file: str = '{:%Y-%m-%d}.log'.format(datetime.now())

    log_file = open(
        f"{PATH_TO_LOG_FILE}app.log", "r"
    )

    log_dictionary: Dict[str, List[str]] = {"personal_website": []}
    previous_app: str = "personal_website"

    for line in log_file:
        split_colon: List[str] = line.split("|")

        app: str = previous_app

        if len(split_colon) >= 2:
            path_to_file: str = split_colon[1]
            
            if "tool_repository" in path_to_file:
                app = "tools"
            elif "personal_webnsite" in path_to_file:
                app = "personal_website"
                
            if not app in log_dictionary.keys():
                log_dictionary[app] = []

            previous_app = app

        log_dictionary[app].append(line)

    return log_dictionary
