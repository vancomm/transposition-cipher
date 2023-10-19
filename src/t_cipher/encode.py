from email import utils
import random
from collections.abc import Sequence

from . import const, utils


def generate_key(size: int) -> Sequence[int]:
    return random.sample((range(size)), k=size)


def validate_key(key_parts: Sequence[int]) -> Sequence[int]:
    size = len(key_parts)
    cols = range(size)

    assert size >= 2, "key must contain at least 2 values"
    assert set(key_parts) == set(cols), f"key must be a permutation of [0; {size - 1}]"

    return key_parts


def encode(
    text: str, key: Sequence[int], *, fill_chars: Sequence[str] = const.cyrillic
) -> str:
    text = text.upper()

    if padding := (len(text) % len(key)):
        text = utils.pad_right(
            text, len(text) + len(key) - padding, fill_chars=fill_chars
        )

    def transpose_char(i: int) -> str:
        j = i % len(key)
        k = i - j + key[j]
        return text[k]

    res: list[str] = utils.defaultlist(str)

    for j in range(0, len(text), len(key)):
        for i in range(j, len(text)):
            res[i] = transpose_char(i)

    return "".join(res)
