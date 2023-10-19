import itertools
from collections.abc import Mapping, Sequence
from typing import cast

from utils import batched


def decode(
    text: str, size: int, bigram_coefs: Mapping[str, Mapping[str, int]]
) -> list[tuple[int, str]]:
    def evaluate_key(key: Sequence[int]) -> tuple[int, str]:
        t_parts = (
            "".join(part[key[i]] for i in range(size)) for part in batched(text, size)
        )
        out = "".join(t_parts)
        i = 0
        score = 0
        for i in range(len(out) - 2):
            score += bigram_coefs[out[i]][out[i + 1]]
        return score, out

    return sorted(
        (evaluate_key(key) for key in itertools.permutations(range(size))),
        key=lambda t: -t[0],
    )
