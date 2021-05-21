#!/usr/bin/env bash

function run_both() {
    FILE=${1}
    echo
    echo "Chardet file ${FILE} of size $(numfmt --to=iec "$(wc -c "${FILE}")")"
    echo

    ./read_file_with_chardet.py "${FILE}"
}

FILE=${1:?Provide file name as first parameter please}

run_both "${FILE}"
