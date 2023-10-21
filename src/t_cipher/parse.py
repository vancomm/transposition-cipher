import csv
from pathlib import Path
from collections import defaultdict
from collections.abc import Mapping


def read_bigram_coefs(
    path_or_str: Path | str, *, default: int | None = None
) -> Mapping[str, Mapping[str, int]]:
    coefs: dict[str, dict[str, int]] = {}

    match path_or_str:
        case Path() as file:
            pass
        case str() as string:
            file = Path(string)

    with file.open(encoding="utf-8") as reader:
        csvreader = csv.reader(reader)
        header = next(csvreader)
        cols = header[1:-1]  # ignore empty first column and unused last column

        for col in cols:
            if col in coefs:
                raise ValueError(f"column {col} was declared twice")
            coefs[col] = {}

        for i, row in enumerate(csvreader):
            key, *row, _ = row  # ignore unused last column

            if len(row) != len(cols):
                raise ValueError(
                    f"row {i} has invalid length ({len(row)} instead of {len(cols)})"
                )

            key_coefs = {col: int(coef) for col, coef in zip(cols, row)}

            if default is not None:
                factory = lambda: default
                key_coefs = defaultdict(factory, key_coefs)

            coefs[key] = key_coefs

    return coefs
