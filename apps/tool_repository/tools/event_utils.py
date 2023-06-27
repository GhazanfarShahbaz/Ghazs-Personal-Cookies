from copy import copy
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple
from pytz import timezone

from dateutil.relativedelta import relativedelta

from apps.tool_repository.tools.repository.events import EventRepository
from apps.tool_repository.tools.repository.models.event_model import Event

# Timezone for dates
NEWYORK_TZ: timezone = timezone("America/New_York")

WEEKDAY: Dict[str, int] = {"m": 0, "t": 1, "w": 2, "th": 3, "f": 4, "sat": 5, "sun": 6}

WEEKNUM: Dict[int, str] = {0: "m", 1: "t", 2: "w", 3: "th", 4: "f", 5: "sat", 6: "sun"}

# Accepted request date formats
DATE_FORMATS: Tuple[str] = (
    "%m/%d/%y %H:%M",
    "%m-%d-%y %H:%M",
    "%m.%d.%y %H:%M",
    "%m/%d/%y %I:%M %p",
    "%m-%d-%y %I:%M %p",
    "%m.%d.%y %I:%M %p",
    "%m/%d/%y %I:%M%p",
    "%m-%d-%y %I:%M%p",
    "%m.%d.%y %I:%M%p",
    "%m/%d/%Y %H:%M",
    "%m-%d-%Y %H:%M",
    "%m.%d.%Y %H:%M",
    "%m/%d/%Y %I:%M %p",
    "%m-%d-%Y %I:%M %p",
    "%m.%d.%Y %I:%M %p",
    "%m/%d/%Y %I:%M%p",
    "%m-%d-%Y %I:%M%p",
    "%m.%d.%Y %I:%M%p",
)


def create_event_information(event_data: dict) -> List[Event]:
    """
    Create a list of events from a request.

    This function takes a dictionary representing the event data from a request and generates a list of events based
    on the data. If the event is a one-off event, it creates a single event. If the event is a recurring event, it creates
    multiple events based on the recurrence settings.

    Args:
        event_data: A dictionary representing the event data from a request.

    Returns:
        A list of Event objects representing the events generated from the request data.

    Raises:
        ValueError: If the event_data dictionary is missing any required fields.
    """

    # Check that required fields are present
    required_fields = [
        "Name",
        "Type",
        "Location",
        "Description",
        "StartDate",
        "EndDate",
    ]
    if not all(field in event_data for field in required_fields):
        raise ValueError("Missing required field in event_data dictionary")

    event_list: List[dict] = []

    # Create event data template
    event_template = {
        "Name": event_data.get("Name"),
        "Type": event_data.get("Type"),
        "Location": event_data.get("Location"),
        "Description": event_data.get("Description"),
    }

    if not event_data.get("RecurranceType"):
        # Single event - no recurrence
        start_date: datetime = string_to_date(event_data.get("StartDate"))
        end_date: datetime = string_to_date(event_data.get("EndDate"))

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        event_template["StartDate"] = start_date
        event_template["EndDate"] = end_date
        event_list.append(event_template)
    else:
        # Recurring event - create list of events
        reccurance_id: int = EventRepository().get_reccurance_count()

        event_template["ReccuranceId"] = reccurance_id
        event_data["RecurranceType"] = event_data["RecurranceType"].lower()

        if event_data["RecurranceType"] not in {"weekly", "monthly", "yearly"}:
            # Daily recurrence
            event_list = get_daily_reccurance_event_list(
                event_template,
                event_data["StartDate"],
                event_data["EndDate"],
                event_data["RecurranceType"],
                event_data["RecurranceDateTo"],
            )
        else:
            # Weekly, monthly, or yearly recurrence
            event_template["RecurranceType"] = event_data["RecurranceType"]
            event_list = get_other_reccurance_event_list(
                event_template,
                event_data["StartDate"],
                event_data["EndDate"],
                event_data["RecurranceType"],
                event_data["RecurranceDateTo"],
            )

    return event_dict_list_to_event_type_list(event_list)


def get_daily_reccurance_event_list(
    event_template: dict,
    start_date: str,
    end_date: str,
    reccurance_type: str,
    reccurance_end_date_string: str,
) -> List[dict]:
    """
    Creates a list of events from one start date to another for daily events.

    This function takes a dictionary representing an event template, a start date, an end date, a recurrence type, and a recurrence
    end date, and generates a list of recurring events based on the event template and recurrence settings.

    Args:
        event_template: A dictionary representing the event template.
        start_date: A string representing the start date for the generated events.
        end_date: A string representing the end date for the generated events.
        recurrence_type: A string representing the type of recurrence ("daily", or a list of weekday abbreviations separated by slashes, such as "m/w/f").
        recurrence_end_date_string: A string representing the end date for recurrence.

    Returns:
        A list of dictionaries, with each dictionary representing an event.
    """

    reccurance_nums: Set[int] = set()

    if reccurance_type == "daily":
        reccurance_nums = {0, 1, 2, 3, 4, 5, 6}
    else:
        "Example:  m/t/th"
        for reccurance_str in reccurance_type.split("/"):
            reccurance_str = reccurance_str.strip().lower()
            global WEEKDAY

            if WEEKDAY.get(reccurance_str):
                reccurance_nums.add(WEEKDAY[reccurance_str])

    if reccurance_type != "daily":
        reccurance_type = ""
        for day in sorted(reccurance_nums):
            reccurance_type += (
                f"/{WEEKNUM[day]}" if reccurance_type else f"{WEEKNUM[day]}"
            )

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
        if current_date.WEEKDAY() in reccurance_nums:
            insertion_start_date: datetime = datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                start_date_hour,
                start_date_minute,
            )
            insertion_end_date: datetime = datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                end_date_hour,
                end_date_minute,
            )
            event = copy(event_template)
            event["StartDate"] = insertion_start_date
            event["EndDate"] = insertion_end_date
            event_list.append(event)

        current_date += time_delta
    return event_list


def get_other_reccurance_event_list(
    event_template: dict,
    start_date: str,
    end_date: str,
    reccurance_type: str,
    reccurance_end_date_string: str,
) -> List[Dict[datetime, datetime]]:
    """
    Generates a list of recurring events for a specified date range.

    This function takes a dictionary representing an event template, a start date, an end date, a recurrence type, and a recurrence
    end date, and generates a list of recurring events based on the event template and recurrence settings.

    Args:
        event_template: A dictionary representing the event template.
        start_date: A string representing the start date for the generated events.
        end_date: A string representing the end date for the generated events.
        recurrence_type: A string representing the type of recurrence ("weekly", "monthly", or "yearly").
        recurrence_end_date_string: A string representing the end date for recurrence.

    Returns:
        A list of dictionaries, with each dictionary representing an event.

    """

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
    reccurance_type = event_template["RecurranceType"]

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
        insertion_start_date: datetime = datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            start_date_hour,
            start_date_minute,
        )
        insertion_end_date: datetime = datetime(
            current_date.year,
            current_date.month,
            current_date.day,
            end_date_hour,
            end_date_minute,
        )
        event = copy(event_template)
        event["StartDate"] = insertion_start_date
        event["EndDate"] = insertion_end_date
        event_list.append(event)

        current_date += time_delta

    return event_list


def string_to_date(date_string: str) -> datetime:
    """
    Convert a date string to a datetime object.

    This function takes a string representing a date and attempts to convert it to a datetime object.
    It tries to match the input string to a set of supported date formats.

    Args:
        date_string: A string representing a date.

    Returns:
        A datetime object representing the input date.

    Raises:
        ValueError: If the input date string is not in a supported format.
    """
    date_string = date_string.strip()

    global DATE_FORMATS
    for date_format in DATE_FORMATS:
        try:
            date: datetime = datetime.strptime(date_string, date_format)
            return date
        except:
            pass

    raise ValueError("This is not a valid date format")


def default_form_get_date_to_and_date_from(
    default_option: str,
) -> Tuple[datetime, datetime]:
    """
    Gets start and end dates from a user request form using a default option.

    This function takes a string representing the default option and uses it to determine the start and end dates.
    If the default option is "today", the start date is set to the beginning of the current day and the end date is set
    to the end of the current day. If the default option is "week", the start date is set to the beginning of the current
    week and the end date is set to the end of the current week. If the default option is "month", the start date is set
    to the beginning of the current month and the end date is set to the end of the current month.

    Args:
        default_option: A string representing the default option to be used.

    Returns:
        A Tuple containing a datetime object representing the start date and an optional datetime object
        representing the end date.

    Raises:
        ValueError: If the input default option is not one of "today", "week", or "month".
    """
    current_date: datetime = datetime.now(timezone("America/New_York"))
    date_to: datetime = None

    if default_option == "today":
        date_from = datetime(
            current_date.year, current_date.month, current_date.day, 0, 0, 0
        )
        date_to = datetime(
            current_date.year, current_date.month, current_date.day, 23, 59, 59
        )

    elif default_option == "week":
        end_date: datetime = None

        if current_date.WEEKDAY() != 0:
            current_date -= timedelta(days=current_date.WEEKDAY())
            end_date = current_date + timedelta(days=6)

        date_from = datetime(
            current_date.year, current_date.month, current_date.day, 0, 0, 0
        )
        date_to = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

    elif default_option == "month":
        date_from = datetime(current_date.year, current_date.month, 1, 0, 0)

        end_date: datetime = date_from + relativedelta(months=1)
        end_date -= timedelta(days=1)

        date_to = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
    else:
        raise ValueError(
            "Invalid default option. Accepted options are 'today', 'week', or 'month'"
        )

    return date_from, date_to


def event_dict_list_to_event_type_list(event_list: List[dict]) -> List[Event]:
    """
    Converts a list of dictionaries to a list of Event objects.

    This function takes a list of dictionaries representing events and converts them to a list of Event objects.

    Args:
        event_list: A list of dictionaries representing events.

    Returns:
        A list of Event objects.

    Raises:
        ValueError: If the input contains dictionaries that do not have the correct keys.
    """

    try:
        return [Event(event) for event in event_list]
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid input dictionary: {e}")


def event_type_list_to_event_type_list(event_list: List[Event]) -> List[dict]:
    """
    Converts a list of Event objects to a list of dictionaries.

    This function takes a list of Event objects and converts them to a list of dictionaries.
    Each dictionary represents an event and contains the information about the event.

    Args:
        event_list: A list of Event objects to be converted.

    Returns:
        A list of dictionaries, with each dictionary representing an event.

    Raises:
        TypeError: If the input list contains objects that are not of type Event.
    """

    if not all(isinstance(event, Event) for event in event_list):
        raise TypeError("All items in the list must be of type `Event`")

    return [event.to_dict() for event in event_list]
