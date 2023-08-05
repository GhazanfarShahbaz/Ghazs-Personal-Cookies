""" 
File Name: allowed_params.py
Creator: Ghazanfar Shahbaz
Creaetd: 08/05/2023
Last Updated: 08/05/2023
Description: Provides functionality to check for allowed parameters
Edit Log:
08/05/2023
- Moved over file from leetcode bot
"""

from typing import Dict, Set, Final

DIFFICULTIES: Final[Set[str]] = ("any", "easy", "medium", "hard")

TAGS: Final[Set[str]] = {
    "any",
    "arrays",
    "backtracking",
    "binary_indexed_tree",
    "binary_search",
    "binary_search_tree",
    "bit_manipulation",
    "brain_teaser",
    "breadth_first_search",
    "depth_first_search",
    "design",
    "divide_and_conquer",
    "dynamic_programming",
    "geometry",
    "graph",
    "greedy",
    "hash_table",
    "heap",
    "line_sweep",
    "linked_lists",
    "math",
    "memoization",
    "minimax",
    "ordered_map",
    "queue",
    "random",
    "recursion",
    "rejection_sampling",
    "reservoir_sampling",
    "rolling_hash",
    "segment_tree",
    "sliding_window",
    "sort",
    "stack",
    "string",
    "suffix_array",
    "topological_sort",
    "tree",
    "trie",
    "two_pointers",
    "union_find",
}

SUBSCRIPTION: Final[Dict[str, str]] = {
    "yes": "subscription",
    "no": "not subscription",
    "any": "any",
}

CODECHEF_DIFFICULTIES: Final[Set[str]] = {
    "beginner",
    "easy",
    "medium",
    "hard",
    "challenge",
}

PROBLEM_TYPES: Final[Dict[str, str]] = {
    "euler": "Euler_Data",
    "leetcode": "Leetcode_Data",
    "codechef": "Codechef_Data",
}


def allowed_difficulties(difficulty: str) -> bool:
    """
    Returns True if the given difficulty is allowed, False otherwise.

    Args:
        difficulty (str): The difficulty picked by the user.

    Returns:
        bool: True if the difficulty is allowed, False otherwise.

    from typing import Set, Final
    """
    return difficulty.lower() in DIFFICULTIES


def allowed_tags(tag: str) -> bool:
    """
    Returns True if the given tag is allowed, False otherwise.

    Args:
        tag (str): The tag picked by the user.

    Returns:
        bool: True if the tag is allowed, False otherwise.
    """
    return tag.lower() in TAGS


def allowed_code_chef_difficulty(difficulty: str) -> bool:
    """
    Returns True if the given CodeChef difficulty is allowed, False otherwise.

    Args:
        difficulty (str): The CodeChef difficulty picked by the user.

    Returns:
        bool: True if the CodeChef difficulty is allowed, False otherwise.
    """
    return difficulty.lower() in CODECHEF_DIFFICULTIES


def allowed_subscription(subscription_type: str) -> bool:
    """
    Returns True if the given subscription type is allowed, False otherwise.

    Args:
        subscription_type (str): The subscription type picked by the user.

    Returns:
        bool: True if the subscription type is allowed, False otherwise.
    """
    return subscription_type.lower() in SUBSCRIPTION


def subscription_query(subscription_type: str) -> str:
    """
    Returns the query string for the given subscription type.

    Args:
        subscription_type (str): The subscription type picked by the user.

    Returns:
        str: The query string for the subscription type.
    """
    return SUBSCRIPTION[subscription_type]


def worksheet_name(question_type: str) -> str:
    """
    Returns the name of the worksheet for the given problem type,
    or an empty string if the type is not recognized.

    Args:
        question_type (str): The problem type picked by the user.

    Returns:
        str: The name of the worksheet for the problem type,
             or an empty string if the type is not recognized.
    """
    return PROBLEM_TYPES[question_type] if question_type in PROBLEM_TYPES else ""
