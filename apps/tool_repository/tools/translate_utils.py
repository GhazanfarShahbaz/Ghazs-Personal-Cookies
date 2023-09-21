"""
file_name = translate_utils.py
Creator: Ghazanfar Shahbaz
Last Updated: 07/14/2023
Description: A module used to handle translations using google translate
Edit Log:
07/14/2023
-   Conformed to pylint conventions.
"""

from typing import Dict, Set, Tuple

from google.cloud import translate_v2 as translate


def get_languages_and_abbreviations() -> Tuple[Set[str], Dict[str, str]]:
    """
    Retrieves languages and their abbreviations.

    This function retrieves a list of languages and their abbreviations from
    Google Translate and returns them as a tuple of a set of abbreviations and a
    dictionary of languages to their abbreviations.

    Returns:
        A tuple containing a set of abbreviations and a dictionary of languages to
        their abbreviations.
    """

    abbreviations: Set[str] = set()  # pylint: disable=redefined-outer-name
    languages_to_abbreviations: Dict[str, str] = {}

    client = translate.Client()

    for language_dict in client.get_languages():
        abbreviation: str = language_dict["language"]

        abbreviations.add(abbreviation)
        languages_to_abbreviations[language_dict["name"]] = abbreviation

    return abbreviations, languages_to_abbreviations


abbreviations, language_to_abbreviations = get_languages_and_abbreviations()


def correct_language(
    language: str, response: dict
) -> str:  # pylint: disable=unused-argument
    """
    Corrects the language parameter for API requests.

    This function takes a string `language` and a dictionary `response` and
    determines whether the language parameter in the request is correct.
    If the language parameter is not in the set of abbreviations or dictionary
    of language to abbreviations, this function attempts to find the correct
    abbreviation and returns it.
    If no abbreviation is found, this function returns None.

    Args:
        language: The language parameter in a request.
        response: A dictionary containing the response from an API request.

    Returns:
        A string representing the correct language abbreviation.
    """

    if language and not language in abbreviations:
        if language in language_to_abbreviations:
            return language_to_abbreviations[language]
        return None

    if not language:
        return None

    return language


def translate_line(text: str, source: str, target: str) -> dict:
    """
    Translates a given line of text.

    This function takes a string `text`, a string `source` representing the source
    language,and a string `target` representing the target language.
    The function corrects the source and target language parameters using the `correct_language`
    function and then calls the `client.translate()` method to translate the text from the source
    language to the target language.
    The function then returns a dictionary containing information about the translation.

    Args:
        text: A string representing the text to be translated.
        source: A string representing the source language.
        target: A string representing the target language.

    Returns:
        A dictionary containing information about the translation.
    """

    response: dict = {}
    text = text.strip()
    source = correct_language(source.strip(), response)
    target = correct_language(target.strip(), response)

    client = translate.Client()

    response["translationInformation"] = client.translate(
        text, source_language=source, target_language=target
    )

    return response
