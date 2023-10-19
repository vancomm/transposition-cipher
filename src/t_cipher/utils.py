from math import ceil
from collections import defaultdict
from collections.abc import Generator, Sequence
from typing import MutableMapping


def batched(text: str, size: int) -> Generator[str, None, None]:
    for i in range(0, len(text), size):
        yield text[i : i + size]


def pad_right(text: str, size: int, *, fill_chars: Sequence[str] = " ") -> str:
    if len(text) > size:
        raise ValueError(
            f"cannot pad string {text!r} " f"of length {len(text)} to size {size}"
        )

    if padding := size - len(text):
        if not fill_chars:
            fill_chars = " "

        if (repeats := ceil(padding / len(fill_chars))) > 1:
            fill_chars = "".join(list(fill_chars) * repeats)

        text += "".join(fill_chars[:padding])

    return text


def ez_table(rows: Sequence[Sequence[str]]) -> str:
    max_widths: MutableMapping[int, int] = defaultdict(int)
    for row in rows:
        for i, cell in enumerate(row):
            if (l := len(cell)) > max_widths[i]:
                max_widths[i] = l

    return "\n".join(
        "".join(cell.ljust(max_widths[i] + 1) for i, cell in enumerate(row))
        for row in rows
    )
