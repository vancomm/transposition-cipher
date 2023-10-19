#!/bin/sh

size=9

python3 -um src.t_cipher encode "СВЕРХСЕКРЕТНОЕ СООБЩЕНИЕ" -s "$size" --no-print-key \
    | tee /dev/tty \
    | xargs -I {} python3 -m src.t_cipher decode -k "$size" -l 10 "{}"