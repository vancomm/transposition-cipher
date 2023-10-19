import random
from collections.abc import Sequence

from .const import cyrillic
from .utils import batched, pad_right


def generate_key(size: int) -> Sequence[int]:
    return random.sample((range(size)), k=size)


def validate_key(key_parts: Sequence[int]) -> Sequence[int]:
    size = len(key_parts)
    cols = range(size)

    assert size >= 2, "key must contain at least 2 values"
    assert set(key_parts) == set(cols), f"key must be a permutation of [0; {size - 1}]"

    return key_parts


def encode(
    msg: str, key: Sequence[int], *, fill_chars: Sequence[str] = cyrillic
) -> str:
    msg = msg.upper()
    size = len(key)

    def transpose(val: str) -> str:
        val = pad_right(val, size, fill_chars=fill_chars)
        return "".join(val[i] for i in key)

    return "".join(transpose(part) for part in batched(msg, size))
