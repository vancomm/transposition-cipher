from collections.abc import Sequence

from const import cyrillic
from utils import batched, pad_right


def encode(
    msg: str, key: Sequence[int], *, fill_chars: Sequence[str] = cyrillic
) -> str:
    msg = msg.upper()
    size = len(key)

    if size < 2:
        raise ValueError("key must contain at least 2 values")

    if set(key) != set(range(size)):
        raise ValueError(f"key must be a permutation of values [0; {size - 1}]")

    def transpose(val: str) -> str:
        val = pad_right(val, size, fill_chars=fill_chars)
        return "".join(val[i] for i in key)

    return "".join(transpose(part) for part in batched(msg, size))
