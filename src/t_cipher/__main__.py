import logging

logging.basicConfig(level=logging.DEBUG)

from .cli import cli


if __name__ == "__main__":
    cli()
