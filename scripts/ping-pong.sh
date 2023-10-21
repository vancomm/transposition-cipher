#!/usr/bin/env bash

message="СВЯЩЕННАЯ РИМСКАЯ ИМПЕРИЯ"
size="${1:=4}"

command time -f "Encoding time: %es" \
    t_cipher encode "$message" \
        --key-size "$size" \
        --key-seed 0 |\
    tee /dev/tty |\
    xargs -I {} time -f "Decoding time: %es" \
        t_cipher decode "{}" \
            --key-size "$size" \
            --limit 5 \
            --parallel
