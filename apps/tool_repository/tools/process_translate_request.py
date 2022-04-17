from google.cloud import translate_v2 as translate

from translate_utils import translate_line

import six

def process_translate(translate_form: dict) -> dict:
    return translate_line(translate_form["text"], translate_form["source"], translate_form["target"])