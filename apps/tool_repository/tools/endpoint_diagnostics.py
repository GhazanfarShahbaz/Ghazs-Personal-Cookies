from repository.endpoint_diagnostics import EndpointDiagnosticsRepository
from repository.model import EndpointDiagnostics

from datetime import datetime
from typing import Dict, List

endpoint_dict: Dict[int, any] = {}
current_index: int = 0

def setup_endpoint_diagnostics(endpoint: str, request) -> int:
    endpoint_diagnostics: Dict[str, any] = {
        "Endpoint"  : endpoint,
        "Request"   : request,
        "Date"      : datetime.now(),
    }
    
    endpoint_id: int = current_index
    endpoint_dict[endpoint_id] = endpoint_diagnostics    
    current_index += 1
    
    return endpoint_id


def commit_endpoint_diagnostics(diagnostic_id: int, response, error = "") -> bool:
    endpoint_diagnostics: Dict[str, any] = endpoint_dict[diagnostic_id]
    
    endpoint_diagnostics["Response"] = response 
    endpoint_diagnostics["Error"] = error 
    endpoint_diagnostics["Latency"] = datetime.now() - endpoint_diagnostics["Date"]
    
    EndpointDiagnosticsRepository().insert(EndpointDiagnostics(endpoint_diagnostics))
    del endpoint_dict[diagnostic_id]
    
    return True

def diagnostics_type_list_to_diagnostic_dict_list(diagnostic_list: List[EndpointDiagnostics]):
    return [diagnostic.to_dict() for diagnostic in diagnostic_list]