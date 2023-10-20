from math import ceil
from collections import defaultdict
from collections.abc import Sequence, Iterable
from typing import Callable, overload


class defaultlist[T](list[T]):
    __default_factory: Callable[[], T]

    @overload
    def __init__(self, __default_factory: Callable[[], T]) -> None:
        ...

    @overload
    def __init__(
        self, __default_factory: Callable[[], T], __iterable: Iterable[T]
    ) -> None:
        ...

    def __init__(
        self, __default_factory: Callable[[], T], __iterable: Iterable[T] | None = None
    ) -> None:
        self.__default_factory = __default_factory
        if __iterable:
            list.__init__(self, __iterable)

    def _grow(self, index: int) -> None:
        while len(self) <= index:
            self.append(self.__default_factory())

    def __getitem__(self, index: int) -> T:
        self._grow(index)
        return list.__getitem__(self, index)

    def __setitem__(self, index: int, value: T) -> None:
        self._grow(index)
        return list.__setitem__(self, index, value)




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
