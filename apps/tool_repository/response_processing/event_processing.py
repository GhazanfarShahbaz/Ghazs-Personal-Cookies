from typing import List, Set
from datetime import datetime
from stringcolor import cs as color


def print_events(event_list: List[dict], exclude_attributes: Set[str]) -> None:
    event_string_list: List[str] = []
    for event in event_list:
        event_string_list.append(print_event(event, exclude_attributes))
    return event_string_list

def print_event(event: dict, exclude_attributes: Set[str]) -> None:
    event_string: str = f"{color(event['Name'], 'dodgerblue')} {dates_to_string(event['StartDate'], event['EndDate'])} "

    if "recurrance" not in exclude_attributes:
        event_string += f"recurs {color(event['ReccuranceType'], 'red')} "

    if "type" not in exclude_attributes:
        event_string += f"and is a {color(event['Type'], 'blue3')} type event "

    return event_string

    
def dates_to_string(start_date: datetime, end_date: datetime) -> str:
    if start_date.day == end_date.day and start_date.month == end_date.month and start_date.year == end_date.year:
        return f"{color(start_date.strftime(f'%B %d %Y'), 'grey4')} at {color(start_date.strftime('%I:%M %p'), 'yellow')} - {color(end_date.strftime('%I:%M %p'), 'yellow')} "
    
    return f"{color(start_date.strftime(f'%B %d %Y'), 'grey4')} {color(start_date.strftime('%I:%M %p'), 'yellow')} - {color(end_date.strftime(f'%B %d %Y'), 'grey4')} {color(end_date.strftime('%I:%M %p'), 'yellow')} "