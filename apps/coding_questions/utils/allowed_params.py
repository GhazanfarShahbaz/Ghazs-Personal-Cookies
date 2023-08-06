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

DIFFICULTIES: Final[Set[str]] = ("any", "Easy", "Medium", "Hard")

TAGS: Final[Set[str]] = [
    "Arrays",
    "Hash Table",
    "Linked Lists",
    "Math",
    "Two Pointers",
    "String",
    "Binary Search",
    "Divide and Conquer",
    "Dynamic Programming",
    "Backtracking",
    "Stack",
    "Heap",
    "Greedy",
    "Sort",
    "Bit Manipulation",
    "Tree",
    "Depth First Search",
    "Breadth First Search",
    "Union Find",
    "Graph",
    "Design",
    "Topological Sort",
    "Trie",
    "Binary Indexed Tree",
    "Segment Tree",
    "Binary Search Tree",
    "Recursion",
    "Brain Teaser",
    "Memoization",
    "Queue",
    "Minimax",
    "Reservoir Sampling",
    "Ordered Map",
    "Geometry",
    "Random",
    "Rejection Sampling",
    "Sliding Window",
    "Line Sweep",
    "Rolling Hash",
    "Suffix Array",
]


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
