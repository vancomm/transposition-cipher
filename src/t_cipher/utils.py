from math import ceil
from collections import defaultdict
from collections.abc import Generator, Sequence, Iterable
from typing import SupportsIndex, Callable, TypeVar, Generic
from typing import cast, overload


T = TypeVar("T")


def make_iter(items: T, size: int = -1) -> Generator[T, None, None]:
    if size < 0:
        while True:
            yield items

    for _ in range(size):
        yield items


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
    max_widths: dict[int, int] = defaultdict(int)
    for row in rows:
        for i, cell in enumerate(row):
            if (l := len(cell)) > max_widths[i]:
                max_widths[i] = l

    return "\n".join(
        "".join(cell.ljust(max_widths[i] + 1) for i, cell in enumerate(row))
        for row in rows
    )
