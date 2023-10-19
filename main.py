import random
from pprint import pprint

from encode import encode
from decode import decode
from read import read_bigram_coefs
from config import ru_bigrams_file


def main():
    bigram_coefs = read_bigram_coefs(ru_bigrams_file, default=0)
    fill_chars = random.sample(list(bigram_coefs), k=len(bigram_coefs))

    size = 9
    message = "СВЯЩЕННАЯ РИМСКАЯ ИМПЕРИЯ"

    key = random.sample((range(size)), k=size)

    encoded = encode(message, key, fill_chars=fill_chars)

    candidates = decode(encoded, len(key), bigram_coefs)

    print(f"{message=}")
    print(f"{encoded=}")
    pprint(candidates[:10])


if __name__ == "__main__":
    main()
