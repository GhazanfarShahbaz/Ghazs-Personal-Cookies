""" 
File Name: message_dict.py
Creator: Ghazanfar Shahbaz
Creaetd: 08/05/2023
Last Updated: 08/05/2023
Description: Provides functionality for formatting discord messages
Edit Log:
08/05/2023
- Moved over file from leetcode bot
"""

from typing import Final, Dict, Optional

MESSAGE_SYNTAX: Final[Dict[str, str]] = {
    "c": "c",
    "c++": "cpp",
    "c#": "c",
    "java": "java",
    "python": "py",
    "python3": "py",
    "javascript": "js",
    "ruby": "ruby",
    "swift": "swift",
    "go": "go",
    "scala": "scala",
    "kotlin": "kotlin",
    "rust": "rust",
    "php": "php",
    "typescript": "typescript",
}


def get_language_code(lang: str) -> Optional[str]:
    """
    Returns the language code that corresponds to the given language, 
    or None if the language is not recognized.

    Args:
        lang (str): The name of the language.

    Returns:
        Optional[str]: The language code that corresponds to the given language,
                       or None if the language is not recognized.
    """
    return (
        None
        if lang.lower() not in MESSAGE_SYNTAX
        else MESSAGE_SYNTAX[lang.lower()]
    )


def check_language(lang: str) -> bool:
    """
    Returns whether the given language is currently supported by the bot.

    Args:
        lang (str): The language to check.

    Returns:
        bool: True if the language is supported, False otherwise.
    """
    return lang.lower() in MESSAGE_SYNTAX
