import itertools
from typing import Any

import inflect


def convert_to_plural(word: str):
    p = inflect.engine()
    plural_word = p.plural(word)
    return plural_word
