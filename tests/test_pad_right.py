import pytest

from collections.abc import Sequence

from t_cipher.utils import pad_right


@pytest.mark.parametrize(
    "text, size, fill_chars, expected",
    [
        ("aaa", 5, " ", "aaa  "),
        ("aaa", 8, "12", "aaa12121"),
        ("aaa", 4, "12345678", "aaa1"),
    ],
)
def test_pad_right(text: str, size: int, fill_chars: Sequence[str], expected: str):
    actual = pad_right(text, size, fill_chars=fill_chars)
    assert actual == expected
