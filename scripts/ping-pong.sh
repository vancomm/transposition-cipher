#!/bin/sh

message="СВЕРХСЕКРЕТНОЕ СООБЩЕНИЕ"
size=8

command time -f "Encoding time: %es" \
    python3 -um src.t_cipher encode "$message" \
        --key-size "$size" \
        --no-print-key |\
    tee /dev/tty |\
    xargs -I {} time -f "Decoding time: %es" \
        python3 -m src.t_cipher decode "{}" \
                --key-size "$size" \
                --limit 10 
