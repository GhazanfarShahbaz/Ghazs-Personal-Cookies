from datetime import datetime
from json import load, dump 
from os import getcwd
from os.path import join
from typing import List


PATH_TO_JSON: str = join(getcwd(), "tools", "timeline.json")

year_format: str = '%Y'
date_formats: List[str]= ['%m/%d/%y', '%m.%d.%y', '%m-%d-%y', '%m/%d/%Y', '%m.%d.%Y', '%m-%d-%Y']

def get_timeline_json() -> dict:
    data_file: any = open(PATH_TO_JSON, "r")
    
    return load(data_file)

def date_to_datetime(date_string: str) -> datetime: 
    return datetime.strptime(date_string, '%m/%d/%Y')
        
def convert_to_correct_date_format(date: datetime) -> str:
    return date.strftime("%m/%d/%Y")

def insert_by_date(new_entry: dict, current_data: list) -> dict:
    new_entry_date: datetime = datetime.strptime(new_entry["dateToSortOn"], '%m/%d/%Y')
    sorted_data: List[dict] = []
    added: bool = False 

    for index, current_item in enumerate(current_data):
        current_item_date: datetime =  datetime.strptime(current_item["dateToSortOn"], '%m/%d/%Y')
        
        if new_entry_date <= current_item_date:
            sorted_data.append(new_entry)
            sorted_data += current_data[index:]
            added = True 
            
            break
        else:
            sorted_data.append(current_item)
            
    if not added:
        sorted_data.append(new_entry)
        
    return sorted_data
            
def update_timeline_json(request_data: dict) -> None:
    data_file: any = open(PATH_TO_JSON, "r+")
    current_json: List[dict] = load(data_file)
    data_file.close()
    
    data = {
        "name": request_data["eventName"],
        "description": request_data["eventDescription"],
        "date": request_data["eventDate"],
        "links": []
    }
    
    format_found = False 
    
    for format in date_formats:
        try:
            datetime.strptime(data["date"], format)
            data["date"] = convert_to_correct_date_format(datetime.strptime(data["date"], format))
            data["dateToSortOn"] = data["date"]
            format_found = True 
            data["onlyYear"] = False            
        except ValueError:
            continue
        
        
    if not format_found:
        try: 
            datetime.strptime(data["date"], year_format)
            data["dateToSortOn"] = "12/31/" + data["date"]
            data["onlyYear"] = True            
        except ValueError:
            data["date"] = convert_to_correct_date_format(datetime.now())
            data["dateToSortOn"] = data["date"]
            data["onlyYear"] = False 
                       
                       
    current_json = insert_by_date(data, current_json)
    
    with open(PATH_TO_JSON, 'w') as f: 
        dump(current_json, f)
    
    