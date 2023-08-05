""" 
File Name: process_random_leetcode.py
Creator: Ghazanfar Shahbaz
Creaetd: 08/05/2023
Last Updated: 08/05/2023
Description: Provides functionality for retrieving random leetcode questions
Edit Log:
08/05/2023
- Create file
"""

from apps.coding_questions.utils.allowed_params import (
    allowed_difficulties,
    allowed_tags,
    allowed_subscription,
)

from repository.leetcode_question_repository import LeetCodeQuestionRepository


def process_random_leetcode_request(filter_form: dict) -> str:
    """
    Process random leetcode request based on the provided filter form.

    Args:
        filter_form (dict): A dictionary containing the filter form data.

    Returns:
        str: The link to a randomly selected LeetCode question that matches the filter criteria.
    """

    if filter_form.get("difficulty") and not allowed_difficulties(
        filter_form.get("difficulty")
    ):
        filter_form["difficulty"] = None

    if filter_form.get("tag") and not allowed_tags(filter_form.get("tag")):
        filter_form["tag"] = None

    if filter_form.get("subscription") and not allowed_subscription(
        filter_form.get("subscription")
    ):
        filter_form["subscription"] = None

    with LeetCodeQuestionRepository() as repository:
        return repository.filter_and_get_random(filter_form).link
