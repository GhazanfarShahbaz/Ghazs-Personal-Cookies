from apps.tool_repository.tools.repository.endpoint_diagnostics import EndpointDiagnosticsRepository
from apps.tool_repository.tools.repository.models.endpoint_diagnostics_model import EndpointDiagnostics

from datetime import datetime
from typing import Dict, List
from werkzeug.datastructures import ImmutableMultiDict


# Global dictionary used to store endpoint diagnostics.
# This dictionary maps endpoint IDs to endpoint diagnostic information.
ENDPOINT_DICT: Dict[int, any] = {}

# Global integer used to keep track of the current endpoint ID.
# This integer is used to generate unique endpoint IDs for each request.
CURRENT_INDEX: int = 0


def setup_request(request: dict, path: str) -> None:
    """
    Sets up the request for processing.

    This function takes a request dictionary and a string representing the endpoint path, and 
    sets up the request for processing by adding an endpoint ID to the request and setting up
    diagnostics for the endpoint.

    Args:
        request: A dictionary representing the request.
        path: A string representing the path of the endpoint.

    Returns:
        None.
    """
    
    request_copy = request.args.to_dict()
    request_copy["endpoint_id"] = setup_endpoint_diagnostics(path, request)
    
    request.args = ImmutableMultiDict(request_copy)
    

def setup_endpoint_diagnostics(endpoint: str, request: dict) -> int:
    """
    Sets up diagnostics for the endpoint using a string and the user's request data.

    This function takes a string representing the endpoint and a dictionary representing the 
    user's request data, and sets up diagnostic information for the endpoint in the 
    global `ENDPOINT_DICT`.

    Args:
        endpoint: A string representing the path of the endpoint.
        request: A dictionary representing the user's request data.

    Returns:
        An integer representing the ID of the endpoint.
    """
    
    endpoint_diagnostics: Dict[str, any] = {
        "Endpoint": endpoint,
        "Request": {},
        "Date": datetime.now(),
    }

    global CURRENT_INDEX, ENDPOINT_DICT
    endpoint_id: int = CURRENT_INDEX
    ENDPOINT_DICT[endpoint_id] = endpoint_diagnostics
    CURRENT_INDEX += 1

    return endpoint_id


def  commit_endpoint_diagnostics(diagnostic_id: int, response: dict, error="") -> bool:
    """
    Commits endpoint diagnostics with the new feature diagnostic values.

    This function takes an ID of an endpoint diagnostic, a dictionary representing the response to the
    request, and an optional error message string. It commits the endpoint diagnostics to the database
    with the new feature diagnostic values.

    Args:
        diagnostic_id: An integer representing the ID of the endpoint diagnostic.
        response: A dictionary representing the response to the request.
        error: An optional string representing the error message.

    Returns:
        A boolean indicating whether the diagnostics were successfully committed to the database.

    Raises:
        KeyError: If the input diagnostic ID does not exist in the global `ENDPOINT_DICT`.
    """
    
    global ENDPOINT_DICT
    endpoint_diagnostics: Dict[str, any] = {}
    
    try:
        endpoint_diagnostics: Dict[str, any] = ENDPOINT_DICT[diagnostic_id]
    except KeyError:
        raise KeyError(f"Diagnostic ID {diagnostic_id} does not exist in ENDPOINT_DICT")

    endpoint_diagnostics["Response"] = {}
    endpoint_diagnostics["Error"] = error
    endpoint_diagnostics["Latency"] = datetime.now().timestamp() - endpoint_diagnostics["Date"].timestamp()

    EndpointDiagnosticsRepository().insert(EndpointDiagnostics(endpoint_diagnostics))
    
    del ENDPOINT_DICT[diagnostic_id]

    return True


def diagnostics_type_list_to_diagnostic_dict_list(diagnostic_list: List[EndpointDiagnostics or any], endpoint_counter = False) -> List[dict]:
    """
    Converts a list of EndpointDiagnostics objects to a list of dictionaries or a dictionary.

    This function takes a list of EndpointDiagnostics objects and converts them to a list of dictionaries.
    Each dictionary represents a diagnostic and contains the information about the request and response
    for that diagnostic. 

    Args:
        diagnostic_list: A list of EndpointDiagnostics objects to be converted.
        endpoint_counter: An optional boolean indicating whether to return a dictionary with a list of unique
                          endpoint names and the number of requests for each endpoint.

    Returns:
        A list of dictionaries, or a dictionary containing endpoint names and the number of requests for each endpoint.

    Raises:
        TypeError: If the input list contains objects that are not of type EndpointDiagnostics.
    """
    
    if not endpoint_counter and not all(isinstance(diagnostic, EndpointDiagnostics) for diagnostic in diagnostic_list):
        raise TypeError("All items in the list must be of type `EndpointDiagnostics`")
    
    if not endpoint_counter:
        return [diagnostic.to_dict() for diagnostic in diagnostic_list]
    
    return {row[0]: row[1] for row in diagnostic_list}