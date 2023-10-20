from pathlib import Path
from collections.abc import Sequence

import click

from . import parse
from . import encode as enc
from . import decode as dec
from . import config, const, utils


@click.group
def cli():
    pass


@cli.command
@click.argument("text", type=str)
@click.argument("key_parts", type=int, nargs=-1)
@click.option(
    "-k",
    "--key-size",
    type=int,
    default=4,
    show_default=True,
    help="Generate a random key of supplied size.",
)
@click.option("--print-key/--no-print-key", default=True)
@click.option("-v", "--verbose", is_flag=True)
def encode(
    text: str, key_parts: Sequence[int], key_size: int, verbose: bool, print_key: bool
):
    try:
        if key_parts:
            key = enc.validate_key(key_parts)
        else:
            key = enc.generate_key(key_size)
            if print_key:
                print("".join((str(i) for i in key)))
        encoded = enc.encode(text, key, fill_chars=const.cyrillic)

        if verbose:
            print(
                utils.ez_table(
                    (
                        ("message:", text),
                        ("key:", str(key)),
                        ("encoded:", encoded),
                    )
                )
            )
        else:
            print(encoded)

    except Exception as e:
        print(f"Error: {e}")


@cli.command
@click.argument("message", type=str)
@click.option(
    "-k",
    "--key-size",
    type=int,
    help="Size of the key used to encode message",
)
@click.option(
    "-l",
    "--limit",
    type=int,
    help="Limit the number of results.",
)
@click.option(
    "-b",
    "--bigrams",
    type=click.Path(
        exists=True,
        readable=True,
        file_okay=True,
        dir_okay=False,
        path_type=Path,
    ),
)
def decode(message: str, key_size: int, bigrams: Path | None, limit: int | None):
    if not bigrams:
        bigrams = config.ru_bigrams_file

    try:
        coefs = parse.read_bigram_coefs(bigrams, default=0)
        candidates = dec.decode(message, key_size, coefs)
        candidates = sorted(candidates, key=lambda a: a[0], reverse=True)

        if limit is not None:
            candidates = candidates[:limit]

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

    except Exception as e:
        raise click.ClickException(str(e))
