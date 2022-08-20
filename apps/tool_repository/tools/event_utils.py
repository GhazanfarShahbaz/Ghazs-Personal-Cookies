from copy import copy
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple
from pytz import timezone

from dateutil.relativedelta import relativedelta

from repository.events import EventRepository
from repository.model import Event

newyork_tz = timezone('America/New_York')

weekday: Dict[str, int]= {
    "m": 0,
    "t": 1,
    "w": 2,
    "th": 3,
    "f": 4,    
    "sat": 5,
    "sun": 6
}

weeknum: Dict[int ,str]= {
    0: "m",
    1: "t",
    2: "w",
    3: "th", 
    4: "f",
    5: "sat",
    6: "sun"
}

date_formats: Tuple[str] = ('%m/%d/%y %H:%M', '%m-%d-%y %H:%M',  '%m.%d.%y %H:%M', '%m/%d/%y %I:%M %p', '%m-%d-%y %I:%M %p', '%m.%d.%y %I:%M %p', '%m/%d/%y %I:%M%p', '%m-%d-%y %I:%M%p', '%m.%d.%y %I:%M%p', '%m/%d/%Y %H:%M', '%m-%d-%Y %H:%M',  '%m.%d.%Y %H:%M', '%m/%d/%Y %I:%M %p', '%m-%d-%Y %I:%M %p', '%m.%d.%Y %I:%M %p', '%m/%d/%Y %I:%M%p', '%m-%d-%Y %I:%M%p', '%m.%d.%Y %I:%M%p')

def create_event_information(event_data: dict) -> List[Event]:
    event_list: List[dict]= []

    event_template = {
        "Name": event_data.get("Name"), 
        "Type": event_data.get("Type"),
        "Location": event_data.get("Location"),
        "Description": event_data.get("Description")
    }

    if not event_data.get("RecurranceType"):
        start_date: datetime = string_to_date(event_data.get("StartDate"))
        end_date: datetime = string_to_date(event_data.get("EndDate"))

        if start_date > end_date:
            start_date, end_date = end_date, start_date 

        event_template["StartDate"] = start_date
        event_template["EndDate"] = end_date
        event_list.append(event_template)
    else:
        reccurance_id: int = None 
        reccurance_id = EventRepository().get_reccurance_count()

        event_template["ReccuranceId"] = reccurance_id 

        if event_data["RecurranceType"].lower() not in {"weekly", "monthly", "yearly"}:
            event_list = get_daily_reccurance_event_list(event_template, event_data["StartDate"], event_data["EndDate"], event_data["RecurranceType"],event_data["RecurranceDateTo"])

        else:
            event_template["RecurranceType"] = event_data["RecurranceType"] 
            event_list = get_other_reccurance_event_list(event_template, event_data["StartDate"], event_data["EndDate"], event_data["RecurranceType"],event_data["RecurranceDateTo"])

    return event_dict_list_to_event_type_list(event_list)


def get_daily_reccurance_event_list(event_template: dict, start_date: str, end_date: str, reccurance_type: str, reccurance_end_date_string: str) -> List[dict]:
    reccurance_nums: Set[int] = set()
    
    if reccurance_type == "daily":
        reccurance_nums = {0,1,2,3,4,5,6}
    else:
        for reccurance_str in reccurance_type.split("/"):
            reccurance_str = reccurance_str.strip().lower()
            global weekday

            if weekday.get(reccurance_str):
                reccurance_nums.add(weekday[reccurance_str])

    if reccurance_type != "daily":
        reccurance_type = ""
        for day in sorted(reccurance_nums):
            reccurance_type += f"/{weeknum[day]}" if reccurance_type else f"{weeknum[day]}"
            
    event_template["ReccuranceType"] = reccurance_type

    start_date: datetime = string_to_date(start_date)
    end_date: datetime = string_to_date(end_date)
    start_date_hour: int = start_date.hour
    start_date_minute: int = start_date.minute
    end_date_hour: int = end_date.hour
    end_date_minute: int = end_date.minute

    if end_date < start_date:
        start_date, end_date = end_date, start_date
    
    current_date: datetime = copy(start_date)
    reccurance_end_date: datetime = string_to_date(reccurance_end_date_string)

    event_list: List[dict] = []
    time_delta: timedelta = timedelta(days=1)
    
    while current_date <= reccurance_end_date:
        if current_date.weekday() in reccurance_nums:
            insertion_start_date: datetime = datetime(current_date.year, current_date.month, current_date.day, start_date_hour, start_date_minute)
            insertion_end_date: datetime = datetime(current_date.year, current_date.month, current_date.day, end_date_hour, end_date_minute)
            event = copy(event_template)
            event["StartDate"] = insertion_start_date
            event["EndDate"] = insertion_end_date
            event_list.append(event)

        current_date += time_delta
    return event_list


def get_other_reccurance_event_list(event_template: dict, start_date: str, end_date: str, reccurance_type: str, reccurance_end_date_string: str) -> List[Dict[datetime, datetime]]:
    start_date: datetime = string_to_date(start_date)
    end_date: datetime = string_to_date(end_date)
    start_date_hour: int = start_date.hour
    start_date_minute: int = start_date.minute
    end_date_hour: int = end_date.hour
    end_date_minute: int = end_date.minute

    if end_date < start_date:
        start_date, end_date = end_date, start_date
    
    current_date: datetime = copy(start_date)
    reccurance_end_date: datetime = string_to_date(reccurance_end_date_string)

    time_delta: timedelta or relativedelta = None 
    if reccurance_type == "weekly":
        time_delta = timedelta(weeks=1)
    elif reccurance_type == "monthly":
        time_delta = relativedelta(months=+1)
    elif reccurance_type == "yearly":
        time_delta = relativedelta(years=+1)
    else:
        return []

    event_list: List[Dict[datetime, datetime]] = []

    while current_date <= reccurance_end_date:
        insertion_start_date: datetime = datetime(current_date.year, current_date.month, current_date.day, start_date_hour, start_date_minute)
        insertion_end_date: datetime = datetime(current_date.year, current_date.month, current_date.day, end_date_hour, end_date_minute)
        event = copy(event_template)
        event["StartDate"] = insertion_start_date
        event["EndDate"] = insertion_end_date
        event_list.append(event)

        current_date += time_delta

    return event_list


def string_to_date(date_string: str) -> datetime:
    date_string = date_string.strip()

    global date_formats
    for date_format in date_formats:
        try:
            date: datetime = datetime.strptime(date_string, date_format)
            return date
        except:
            pass
    
    raise ValueError("This is not a valid date format")


def default_form_get_date_to_and_date_from(default_option: str) -> tuple: 
    current_date: datetime = datetime.now(timezone('America/New_York'))
    date_to: datetime = None 
    
    if default_option == "today":
        date_from = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0)
        date_to = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)

    
    elif default_option == "week":
        end_date: datetime = None 

        if current_date.weekday() != 0:
            current_date -= timedelta(days=current_date.weekday())
            end_date = current_date + timedelta(days=6)
        
        date_from = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0)
        date_to =  datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59) 
    
    elif default_option == "month":
        date_from = datetime(current_date.year, current_date.month, 1, 0, 0)

        end_date: datetime = date_from + relativedelta(months=1)
        end_date -= timedelta(days=1)

        date_to =  datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59) 

    return date_from, date_to


def event_dict_list_to_event_type_list(event_list: List[dict]) -> List[Event]:
    return [Event(event) for event in event_list]


def event_type_list_to_event_type_list(event_list: List[Event]) -> List[dict]:
    return [event.to_dict() for event in event_list]    