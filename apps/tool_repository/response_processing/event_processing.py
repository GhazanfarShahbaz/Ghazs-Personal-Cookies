from typing import List, Set
from datetime import datetime
from stringcolor import cs as color


def print_events(event_list: List[dict], exclude_attributes: Set[str]) -> List[str]:
    """
    Prints a list of events as strings, with optional attributes excluded.

    This function takes a list of event dictionaries and a set of attributes to exclude,
    and returns a list of strings representing the events in the list.

    Args:
        event_list: A list of dictionaries representing event data.
        exclude_attributes: A set of attribute names to exclude from the printed output.

    Returns:
        A list of strings representing the events in the input list.
    """
    
    event_string_list: List[str] = []
    for event in event_list:
        event_string_list.append(print_event(event, exclude_attributes))
    return event_string_list


def print_event(event: dict, exclude_attributes: Set[str]) -> str:
    """
    Returns single event as a string, with optional attributes excluded.

    This function takes a dictionary representing an event and a set of attributes to exclude,
    and returns a string representing the event with the specified attributes excluded.

    Args:
        event: A dictionary representing an event.
        exclude_attributes: A set of attribute names to exclude from the printed output.

    Returns:
        A string representing the event with the specified attributes excluded.
    """
    event_string: str = f"{color(event['Name'], 'dodgerblue')} {dates_to_string(event['StartDate'], event['EndDate'])} "

    if "recurrance" not in exclude_attributes:
        event_string += f"recurs {color(event['ReccuranceType'], 'red')} "

    if "type" not in exclude_attributes:
        event_string += f"and is a {color(event['Type'], 'blue3')} type event "

    return event_string


def dates_to_string(start_date: datetime, end_date: datetime) -> str:
    """
    Converts a pair of dates to a string representing a time interval.

    This function takes two dates and returns a string representing the time interval between them.

    Args:
        start_date: A datetime object representing the start of the interval.
        end_date: A datetime object representing the end of the interval.

    Returns:
        A string representing the time interval between the start and end dates.
    """
    
    if start_date.day == end_date.day and start_date.month == end_date.month and start_date.year == end_date.year:
        return f"{color(start_date.strftime(f'%B %d %Y'), 'grey4')} at {color(start_date.strftime('%I:%M %p'), 'yellow')} - {color(end_date.strftime('%I:%M %p'), 'yellow')} "

    return f"{color(start_date.strftime(f'%B %d %Y'), 'grey4')} {color(start_date.strftime('%I:%M %p'), 'yellow')} - {color(end_date.strftime(f'%B %d %Y'), 'grey4')} {color(end_date.strftime('%I:%M %p'), 'yellow')} "
