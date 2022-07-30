from google.cloud import translate_v2 as translate

from typing import Dict, Set, Tuple


def get_languages_and_abbreviations() -> Tuple[Set[str], Dict[str, str]]:
    abbreviations: Set[str] = set()
    languages_to_abbreviations: Dict[str, str] = {}

    client = translate.Client()

    for language_dict in client.get_languages():
        abbreviation: str = language_dict['language']

        abbreviations.add(abbreviation)
        languages_to_abbreviations[language_dict["name"]] = abbreviation

    return abbreviations, languages_to_abbreviations


abbreviations, language_to_abbreviations = get_languages_and_abbreviations()


def correct_language(language: str, response: dict) -> str:
    if language and not language in abbreviations:
        if language in language_to_abbreviations.keys():
            return language_to_abbreviations[language]
        else:
            return None
    elif not language:
        return None

    return language


def translate_line(text: str, source: str, target: str) -> dict:
    response: dict = {}
    text = text.strip()
    source = correct_language(source.strip(), response)
    target = correct_language(target.strip(), response)

    client = translate.Client()

    response["translationInformation"] = client.translate(
        text, source_language=source, target_language=target)

    return response
