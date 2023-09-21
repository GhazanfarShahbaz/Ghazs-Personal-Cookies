from apps.coding_questions.utils.process_random_leetcode import process_random_leetcode_request
from repository.models.leetcode_question_model import LeetCodeQuestion

import pytest

@pytest.fixture
def leetcode_request_fixture(request):
    return {
        "difficulty": None if request.param[0] is None else request.param[0],
        "tag": None if request.param[1] is None else request.param[1],
        "subscription": None if request.param[2] is None else request.param[2]
    }
    
    
@pytest.mark.parametrize("leetcode_request_fixture",[[None, None, None], ["easy", None, None], ["medium", "string", None], ["hard", "array", True]], indirect=True)
def test_process_random_leetcode_request(leetcode_request_fixture):
    question: LeetCodeQuestion = process_random_leetcode_request(leetcode_request_fixture)
    
    assert question is not None 
    
    difficulty: str or None = leetcode_request_fixture["difficulty"]
    tag: str or None = leetcode_request_fixture["tag"]
    subscription: bool or None = leetcode_request_fixture["subscription"]

    if difficulty is not None:
        assert question.difficulty.lower() == difficulty.lower()
        
    if tag is not None:
        assert question.tag.lower() == tag.lower()
        
    if subscription is not None:
        assert question.subscription == subscription