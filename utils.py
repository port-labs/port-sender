import itertools
from typing import Any

import inflect


def convert_to_plural(word: str):
    p = inflect.engine()
    plural_word = p.plural(word)
    return plural_word

def batch_items(items: list[Any], batch_size: int):
    """
    Breaks the given list of items into batched lists with a preset length.

    :param items: List of items to be batched.
    :param batch_size: Preset length of each batch.
    :return: List of batched lists.
    """
    if batch_size <= 0:
        raise ValueError("Batch size must be greater than 0")

    it = iter(items)
    batched_list = list(iter(lambda: list(itertools.islice(it, batch_size)), []))
    
    return batched_list