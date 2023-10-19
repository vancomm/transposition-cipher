import re
import string
from collections.abc import Sequence

import pytest

from encode import encode


@pytest.mark.parametrize(
    "msg, key, expected_pattern",
    [
        ("ABC", (2, 0, 1), r"CAB"),
        ("or it's just fantasy", (1, 3, 4, 2, 0), r"RIT OSJU 'TFA STSYAN"),
    ],
)
def test_encode(msg: str, key: Sequence[int], expected_pattern: str):
    actual = encode(msg, key, fill_chars=string.ascii_uppercase)
    assert re.fullmatch(expected_pattern, actual), f"{actual=}, {expected_pattern=}"


# or it
# 's ju
# st fa
# ntasy
