#!/usr/bin/env bash

function run_both() {
    FILE=${1}
    echo
    echo "Charset normalizer file ${FILE} of size $(numfmt --to=iec "$(wc -c "${FILE}")")"
    echo

    ./read_file_with_charset_normalizer.py "${FILE}"
    echo
}

FILE=${1:?Provide file name as first parameter please}

run_both "${FILE}"
