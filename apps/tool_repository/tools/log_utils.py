from typing import Dict, List

PATH_TO_LOG_FILE: str = "/home/ghaz/flask_gateway/logs/personal_website_requests.log"

def split_up_log_file() -> Dict[str, List[str]]:
    log_file: TextIOWrapper = open(PATH_TO_LOG_FILE, "r")
    
    log_dictionary: Dict[str, List[str]] = {"": []}
    previous_app: str = ""
    
    for line in log_file:
        split_colon: List[str] = line.split(":")

        app: str = previous_app 
        
        if split_colon[0] == "INFO":
            split_dot: List[str] = split_colon[1].split(".")
            if split_dot[0] == "apps":
                app = split_dot[1]
                
                if not app in log_dictionary.keys():
                    log_dictionary[app] = []
                
                previous_app = app
            
        log_dictionary[app].append(line)
