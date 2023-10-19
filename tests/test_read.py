from pathlib import Path
from collections.abc import Mapping

import pytest

from t_cipher.parse import read_bigram_coefs


@pytest.mark.parametrize(
    "file, expected",
    [
        (
            Path("tests/files/bigrams_s.csv"),
            {
                "A": {"A": 1, "B": 2, "C": 3},
                "B": {"A": 4, "B": 5, "C": 6},
                "C": {"A": 7, "B": 8, "C": 9},
            },
        ),
    ],
)
def test_read_bigram_coefs(file: Path, expected: Mapping[str, Mapping[str, int]]):
    actual = read_bigram_coefs(file)
    assert actual == expected
