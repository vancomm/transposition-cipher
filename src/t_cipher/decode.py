import logging
import itertools
from collections.abc import Mapping, Sequence
from typing import Iterable


def decode(
    text: str, key_size: int, bigram_coefs: Mapping[str, Mapping[str, int]]
) -> Iterable[tuple[int, str]]:
    len_text = len(text)

    if len_text % key_size != 0:
        raise ValueError(
            f"cannot decode text {text} of length {len_text} (must be a multiple of {key_size=})"
        )

    def evaluate_key(key: Sequence[int]) -> tuple[int, str]:
        def transpose_char(i: int) -> str:
            j = i % key_size
            k = i - j + key[j]
            return text[k]

        score = 0
        chars: list[str] = [""] * len_text

        for i in range(len_text):
            if i % 2 == 0:
                chars[i] = transpose_char(i)
                if i + 1 < len_text:
                    chars[i + 1] = transpose_char(i + 1)
                    try:
                        s = bigram_coefs[chars[i]][chars[i + 1]]
                        score += s
                    except Exception as e:
                        logging.info(e, stack_info=True)
                        print(repr(e))
                        print(chars)
                        print(chars[i], chars[i + 1])
                        quit()

            pass

        return score, "".join(chars)

    entries = (evaluate_key(key) for key in itertools.permutations(range(key_size)))

    return entries
