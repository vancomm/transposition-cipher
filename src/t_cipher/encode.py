import random
from collections.abc import Sequence

from . import const, utils


def generate_key(
    size: int, *, seed: int | float | str | bytes | bytearray | None = None
) -> Sequence[int]:
    random.seed(seed)
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
    len_key = len(key)

    if padding := (len(text) % len_key):
        text = utils.pad_right(
            text, len(text) + len_key - padding, fill_chars=fill_chars
        )

    text = text.upper()
    len_text = len(text)

    def transpose_char(i: int) -> str:
        j = i % len_key
        k = i - j + key[j]
        return text[k]

    res: list[str] = [""] * len_text

    for j in range(0, len_text, len_key):
        for i in range(j, len_text):
            res[i] = transpose_char(i)

    return "".join(res)
