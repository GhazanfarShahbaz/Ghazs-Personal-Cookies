from endpoint_diagnostics import setup_endpoint_diagnostics, commit_endpoint_diagnostics, diagnostics_type_list_to_diagnostic_dict_list
from apps.tool_repository.tools.repository.models.endpoint_diagnostics_model import EndpointDiagnostics
from apps.tool_repository.tools.repository.endpoint_diagnostics import EndpointDiagnosticsRepository
from event_utils import string_to_date

from typing import Dict, List


def process_commit_diagnostics(diagnostic_id: None or int, endpoint_info: Dict[str, str]) -> int:
    if diagnostic_id is None:
        return setup_endpoint_diagnostics(endpoint=endpoint_info["Endpoint"], request=endpoint_info["Request"])

    commit_endpoint_diagnostics(diagnostic_id=diagnostic_id,
                                response=endpoint_info["Response"], error=endpoint_info["Error"])


def process_get_diagnostics(diagnostic_filter_form: Dict[str, str]) -> List[Dict[str, any]]:
    diagnostic_filter_form["DateFrom"] = string_to_date(diagnostic_filter_form["DateFrom"])
    diagnostic_filter_form["DateTo"] = string_to_date(diagnostic_filter_form["DateTo"])

    
    endpoint_diagnostics: Dict[EndpointDiagnostics] = EndpointDiagnosticsRepository(
    ).get(filters=diagnostic_filter_form)

    return diagnostics_type_list_to_diagnostic_dict_list(diagnostic_list=endpoint_diagnostics, endpoint_counter=diagnostic_filter_form.get("EndpointCounter"))
