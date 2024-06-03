"""
file_name = event_processing.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/08/2023
Description: A module used to process event data and turn it into a string.
Edit Log:
07/14/2023 
-   Conformed to pylint conventions
"""

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

    This function takes a dictionary representing an event and a set of
    attributes to exclude, and returns a string representing the event with
    the specified attributes excluded.

    Args:
        event: A dictionary representing an event.
        exclude_attributes: A set of attribute names to exclude from the printed output.

    Returns:
        A string representing the event with the specified attributes excluded.
    """
    event_string: str = f"{color(event['Name'], 'dodgerblue')} {dates_to_string(event['StartDate'], event['EndDate'])} "  # pylint: disable=line-too-long

    if "recurrance" not in exclude_attributes:
        event_string += f"recurs {color(event['ReccuranceType'], 'red')} "

    if "type" not in exclude_attributes:
        event_string += f"and is a {color(event['Type'], 'blue3')} type event "

    return event_string


def date_to_date_string(date: datetime) -> str:
    return date.strftime(f'%B %d %Y')


def date_to_time_string(date: datetime) -> str:
    return date.strftime('%I:%M %p')


def dates_to_string(start_date: datetime, end_date: datetime) -> str:
    """
    Converts a pair of dates to a string representing a time interval.

    This function takes two dates and returns a string representing the time
    interval between them.

    Args:
        start_date: A datetime object representing the start of the interval.
        end_date: A datetime object representing the end of the interval.

    Returns:
        A string representing the time interval between the start and end dates.
    """ 
    
    start_date_string: str = date_to_date_string(start_date)
    start_time_string: str = date_to_time_string(start_date)
    end_time_string: str = date_to_time_string(end_date)
    
    if (
        start_date.day == end_date.day
        and start_date.month == end_date.month
        and start_date.year == end_date.year
    ):
        return f"{color(start_date_string, 'grey4')} at {color(start_time_string, 'yellow')} - {color(end_time_string, 'yellow')} "  # pylint: disable=line-too-long, f-string-without-interpolation

    end_date_string: str = date_to_date_string(end_date)
    
    return f"{color(start_date_string, 'grey4')} {color(start_time_string, 'yellow')} - {color(end_date_string, 'grey4')} {color(end_time_string, 'yellow')} "  # pylint: disable=line-too-long, f-string-without-interpolation


def jsonify_event_list(event_list: List[dict]) -> dict:
    jsonified_list: List[dict] = []
    
    for event in event_list:
        current_item = {
            "Id":               event["Id"],
            "RecurrenceId":     event["ReccuranceId"],
            "Name":             event["Name"],
            "StartDate":        date_to_date_string(event["StartDate"]),
            "StartTime":        date_to_time_string(event["StartDate"]),
            "EndDate":          date_to_date_string(event["EndDate"]),
            "EndTime":          date_to_time_string(event["EndDate"]),
            "Description":      event["Description"],
            "RecurrenceType":   event["ReccuranceType"],
            "Location":         event["Location"],
        }
        
        jsonified_list.append(current_item)
        
    return {"events": jsonified_list}
    