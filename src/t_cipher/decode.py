import pathlib
import itertools
import multiprocessing as mp
from collections.abc import Mapping, Sequence, Iterable

from . import parse


def evaluate_key(
    text: str,
    key: Sequence[int],
    bigram_coefs: Mapping[str, Mapping[str, int]],
) -> tuple[int, str]:
    len_text = len(text)
    len_key = len(key)

    match bigram_coefs:
        case pathlib.Path() | str() as bigram_file:
            coefs = parse.read_bigram_coefs(bigram_file, default=0)
        case coefs:
            pass

    def transpose_char(i: int) -> str:
        j = i % len_key
        k = i - j + key[j]
        return text[k]

    score = 0
    chars: list[str] = [""] * len_text

    for i in range(len_text):
        if i % 2 == 0:
            chars[i] = transpose_char(i)
            if i + 1 < len_text:
                chars[i + 1] = transpose_char(i + 1)
                s = coefs[chars[i]][chars[i + 1]]
                score += s

    return score, "".join(chars)


def decode(
    text: str,
    key_size: int,
    bigrams: Mapping[str, Mapping[str, int]] | pathlib.Path | str,
) -> Iterable[tuple[int, str]]:
    if len(text) % key_size != 0:
        raise ValueError(
            f"cannot decode text {text} of length {len(text)} "
            f"(must be a multiple of {key_size=})"
        )

    if isinstance(bigrams, (pathlib.Path, str)):
        coefs = parse.read_bigram_coefs(bigrams, default=0)
    else:
        coefs = bigrams

    keys = itertools.permutations(range(key_size))
    entries = (evaluate_key(text, key, coefs) for key in keys)

    return list(entries)


def _init_work(__work, text: str, coefs: Mapping[str, Mapping[str, int]]) -> None:
    __work._text = text
    __work._coefs = coefs


def _work(key: Sequence[int]) -> tuple[int, str]:
    return evaluate_key(_work._text, key, _work._coefs)


def decode_parallel(
    text: str, key_size: int, bigram_file: pathlib.Path | str
) -> Iterable[tuple[int, str]]:
    keys = itertools.permutations(range(key_size))
    coefs = parse.read_bigram_coefs(bigram_file, default=0)

    with mp.Pool(initializer=_init_work, initargs=(_work, text, coefs)) as p:
        return p.map(_work, keys)
