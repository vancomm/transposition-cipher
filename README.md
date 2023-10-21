# t_cipher

```
Usage: t_cipher [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  decode  Decode MESSAGE encoded with a key of KEY_SIZE.
  encode  Encode MESSAGE with key from KEY_PARTS or a random one.
```

## Encode

```
Usage: t_cipher encode [OPTIONS] MESSAGE [KEY_PARTS]...

  Encode MESSAGE with key from KEY_PARTS or a random one.

Options:
  -k, --key-size INTEGER  Generate a random key of supplied size.  [default:
                          4]
  -s, --key-seed TEXT     Seed PRNG for key generation.
  -p, --print-key         Toggle key output.
  -v, --verbose           Toggle verbose output.
  -h, --help              Show this message and exit.
```

## Decode

```
Usage: t_cipher decode [OPTIONS] MESSAGE

  Decode MESSAGE encoded with a key of KEY_SIZE.

Options:
  -k, --key-size INTEGER  Size of the key used to encode message
  -l, --limit INTEGER     Limit the number of results.
  -b, --bigrams FILE      Provide a custom bigram file for candidate scoring.
  -p, --parallel          Use multiprocessing.
  -h, --help              Show this message and exit.

```