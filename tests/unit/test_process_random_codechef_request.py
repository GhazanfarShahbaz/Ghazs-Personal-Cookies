from apps.coding_questions.utils.process_random_codechef_question import process_random_codechef_request

from repository.models.codechef_question_model import CodeChefQuestion

import pytest

@pytest.fixture
def codechef_request_fixture(request):
    yield {
        "difficulty": None if request.param[0] is None else request.param[0],
    }
    
    
@pytest.mark.parametrize("codechef_request_fixture",[[None], ["beginner"], ["easy"], ["beginner"], ["medium"], ["hard"], ["challenge"]], indirect=True)
def test_process_random_codechef_request(codechef_request_fixture):
    question: CodeChefQuestion = process_random_codechef_request(codechef_request_fixture)
    
    assert question is not None 
    
    difficulty: str or None = codechef_request_fixture["difficulty"]

    if difficulty is not None:
        assert question.difficulty.lower() == difficulty[0].lower()
