import itertools
from collections.abc import Mapping, Sequence


def decode(
    text: str, key_size: int, bigram_coefs: Mapping[str, Mapping[str, int]]
) -> list[tuple[int, str]]:
    len_text = len(text)

    def evaluate_key(key: Sequence[int]) -> tuple[int, str]:
        def transpose_char(i: int) -> str:
            j = i % key_size
            return text[i - j + key[j]]

        score = 0
        chars = [""] * len_text

        for i in range(len_text):
            if i % 2 == 0:
                chars[i] = transpose_char(i)
                if i + 1 < len_text:
                    chars[i + 1] = transpose_char(i + 1)
                    score += bigram_coefs[chars[i]][chars[i + 1]]

        return score, "".join(chars)

    return sorted(
        (evaluate_key(key) for key in itertools.permutations(range(key_size))),
        key=lambda t: -t[0],
    )
