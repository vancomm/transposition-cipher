import logging
from pathlib import Path
from collections.abc import Sequence

import click

from . import parse
from . import encode as enc
from . import decode as dec
from . import config, const, utils


logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli() -> None:
    pass


@cli.command
@click.argument("message", type=str)
@click.argument("key_parts", type=int, nargs=-1)
@click.option(
    "-k",
    "--key-size",
    type=int,
    default=4,
    show_default=True,
    help="Generate a random key of supplied size.",
)
@click.option(
    "-s",
    "--key-seed",
    type=str,
    help="Seed PRNG for key generation.",
)
@click.option(
    "-p",
    "--print-key",
    is_flag=True,
    default=False,
    show_default=True,
    help="Toggle key output.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    show_default=True,
    help="Toggle verbose output.",
)
def encode(
    message: str,
    key_parts: Sequence[int],
    key_size: int,
    key_seed: str | None,
    print_key: bool,
    verbose: bool,
) -> None:
    """
    Encode MESSAGE with key from KEY_PARTS or a random one.
    """
    try:
        if key_parts:
            key = enc.validate_key(key_parts)
        else:
            key = enc.generate_key(key_size, seed=key_seed)

        if print_key:
            print("".join((str(i) for i in key)))

        encoded = enc.encode(message, key, fill_chars=const.cyrillic)

        if verbose:
            print(
                utils.ez_table(
                    (
                        ("message:", message),
                        ("key:", str(key)),
                        ("encoded:", encoded),
                    )
                )
            )
        else:
            print(encoded)

    except Exception as e:
        logger.error(e, stack_info=True)
        raise click.ClickException(str(e))


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
    help="Provide a custom bigram file for candidate scoring.",
)
@click.option("-p", "--parallel", is_flag=True, help="Use multiprocessing.")
def decode(
    message: str,
    key_size: int,
    bigrams: Path | None,
    limit: int | None,
    parallel: bool,
) -> None:
    """
    Decode MESSAGE encoded with a key of KEY_SIZE.
    """
    if not bigrams:
        bigrams = config.ru_bigrams_file

    try:
        if parallel:
            candidates = dec.decode_parallel(message, key_size, bigrams)
        else:
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
        logger.error(e, stack_info=True)
        raise click.ClickException(str(e))
