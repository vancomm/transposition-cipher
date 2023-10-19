#!/bin/sh

python3 -um src.t_cipher encode "СВЕРХСЕКРЕТНОЕ СООБЩЕНИЕ" -s 6 | \
    tee /dev/tty | \
    xargs -I {} python3 -m src.t_cipher decode -k 6 -l 25 "{}"