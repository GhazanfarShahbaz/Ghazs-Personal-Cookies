""" 
File Name: process_random_codechef_question.py
Creator: Ghazanfar Shahbaz
Creaetd: 08/05/2023
Last Updated: 08/05/2023
Description: Provides functionality for retrieving random codechef questions
Edit Log:
08/05/2023
- Create file
"""

from apps.coding_questions.utils.allowed_params import allowed_code_chef_difficulty

from repository.codechef_question_repository import CodeChefQuestionRepository


def process_random_codechef_request(filter_form: dict) -> str:
    """
    Process a random CodeChef request based on the provided filter form.

    Args:
        filter_form (dict): A dictionary containing the filter form data.

    Returns:
        str: The link to a randomly selected CodeChef question that matches the filter criteria.

    """
    
    if filter_form.get("difficulty"):
        filter_form["difficulty"] = filter_form["difficulty"].lower()
        if not allowed_code_chef_difficulty(filter_form.get("difficulty")):
            filter_form["difficulty"] = None

    with CodeChefQuestionRepository() as repository:
        return repository.filter_and_get_random(filter_form).link
