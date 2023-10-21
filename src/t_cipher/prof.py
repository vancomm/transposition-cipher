#!/usr/bin/env python3

import random
import cProfile
import pstats
from pathlib import Path

from . import encode as enc
from . import decode as dec
from . import parse
from . import config, utils


def run() -> None:
    bigram_coefs = parse.read_bigram_coefs(config.ru_bigrams_file, default=0)
    fill_chars = random.sample(list(bigram_coefs), k=len(bigram_coefs))

    size = 4
    message = "СВЯЩЕННАЯ РИМСКАЯ ИМПЕРИЯ"

    key = enc.generate_key(size)
    encoded = enc.encode(message, key, fill_chars=fill_chars)

    print(
        utils.ez_table(
            (
                ("message:", message),
                ("key:", str(key)),
                ("encoded:", encoded),
            )
        )
    )

    candidates = dec.decode(encoded, size, bigram_coefs)
    candidates = sorted(candidates, reverse=True)
    candidates = candidates[:5]

    print(
        utils.ez_table(
            (
                ("#", "Candidate", "Score"),
                *(
                    (str(i + 1), text, str(score))
                    for i, (score, text) in enumerate(candidates)
                ),
            )
        )
    )


def main() -> None:
    prof_dir = Path("./prof")
    prof_dir.mkdir(exist_ok=True)

    with cProfile.Profile() as pr:
        run()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(prof_dir / "stats.prof")
    print("== Profiling stats =====================================")
    stats.print_stats(3)


if __name__ == "__main__":
    main()
