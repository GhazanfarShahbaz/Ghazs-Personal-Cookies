from google.cloud import translate_v2 as translate

from typing import Dict, Set, Tuple

import six

def get_languages_and_abbreviations() -> tuple:
    abbreviations: Set[str] = set()
    languages_to_abbreviations: Dict[str, str] = {}
    
    client = translate.Client()
    
    for language_dict in client.get_languages():
        abbreviation: str = language_dict['language']
        
        abbreviations.add(abbreviation)
        languages_to_abbreviations[language_dict["name"]] = abbreviation
        
    
    return abbreviations, languages_to_abbreviations


    