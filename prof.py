import random
import cProfile
import pstats
from pathlib import Path
from pprint import pprint

import sys

sys.path.insert(0, "./src")  # import hack

from t_cipher import encode as enc
from t_cipher import decode as dec
from t_cipher import parse
from t_cipher import config, utils


def run() -> None:
    bigram_coefs = parse.read_bigram_coefs(config.ru_bigrams_file, default=0)
    fill_chars = random.sample(list(bigram_coefs), k=len(bigram_coefs))

    size = 9
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
    candidates = sorted(candidates)
    candidates = candidates[:5]

    pprint(candidates)


def main() -> None:
    prof_dir = Path("./prof")
    prof_dir.mkdir(exist_ok=True)

    with cProfile.Profile() as pr:
        run()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(prof_dir / "stats.prof")
    stats.print_stats(3)


if __name__ == "__main__":
    main()
