from pathlib import Path
from datetime import datetime
import cProfile
import pstats

import main as m


def main():
    with cProfile.Profile() as pr:
        m.main()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(Path(f"./prof/stats.prof"))
    stats.print_stats()


if __name__ == "__main__":
    main()
