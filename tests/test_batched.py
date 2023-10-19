import pytest
from utils import batched


@pytest.mark.parametrize(
    "text, size, expected",
    [
        ("is it real life", 3, ("is ", "it ", "rea", "l l", "ife")),
        ("abcdef", 4, ("abcd", "ef")),
    ],
)
def test_batched(text: str, size: int, expected: tuple[str]):
    actual = tuple(batched(text, size))
    assert actual == expected
