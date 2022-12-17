from repository.endpoint_diagnostics import EndpointDiagnosticsRepository
from repository.model import EndpointDiagnostics

from datetime import datetime
from typing import Dict, List

ENDPOINT_DICT: Dict[int, any] = {}
CURRENT_INDEX: int = 0


def setup_endpoint_diagnostics(endpoint: str, request) -> int:
    endpoint_diagnostics: Dict[str, any] = {
        "Endpoint": endpoint,
        "Request": request,
        "Date": datetime.now(),
    }

    global CURRENT_INDEX, ENDPOINT_DICT
    endpoint_id: int = CURRENT_INDEX
    ENDPOINT_DICT[endpoint_id] = endpoint_diagnostics
    CURRENT_INDEX += 1

    return endpoint_id


def commit_endpoint_diagnostics(diagnostic_id: int, response, error="") -> bool:
    global ENDPOINT_DICT
    endpoint_diagnostics: Dict[str, any] = ENDPOINT_DICT[diagnostic_id]

    endpoint_diagnostics["Response"] = response
    endpoint_diagnostics["Error"] = error
    endpoint_diagnostics["Latency"] = datetime.now() - \
        endpoint_diagnostics["Date"]

    with EndpointDiagnosticsRepository() as repository:
        repository.insert(EndpointDiagnostics(endpoint_diagnostics))
    
    del ENDPOINT_DICT[diagnostic_id]

    return True


def diagnostics_type_list_to_diagnostic_dict_list(diagnostic_list: List[EndpointDiagnostics]):
    return [diagnostic.to_dict() for diagnostic in diagnostic_list]
