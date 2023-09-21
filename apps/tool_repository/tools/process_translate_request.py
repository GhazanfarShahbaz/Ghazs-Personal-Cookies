"""
file_name = process_translate_requests.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to translate requests.
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

from apps.tool_repository.tools.translate_utils import translate_line


def process_translate(translate_form: dict) -> dict:
    """
    Processes a translation request.

    This function takes a dictionary `translate_form` containing the text to be translated,
    the source language, and the target language.
    It then calls the `translate_line` function with these parameters to perform the translation
    and returns a dictionary containing the translated text.

    Args:
        translate_form: A dictionary containing the text to be translated, the source language,
        and the target language.

    Returns:
        A dictionary containing the translated text.
    """

    return translate_line(
        translate_form["text"], translate_form["source"], translate_form["target"]
    )
