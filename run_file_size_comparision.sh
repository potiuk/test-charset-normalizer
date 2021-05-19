#!/usr/bin/env bash

function run_both() {
    FILE=${1}
    echo
    echo "Comparing file ${FILE} of size $(numfmt --to=iec "$(wc -c "${FILE}")")"
    echo

    echo
    echo "Chardet"
    echo
    ./read_file_with_chardet.py "${FILE}"

    echo
    echo "Charset normalizer"
    echo
    ./read_file_with_charset_normalizer.py "${FILE}"
    echo
}

FILE=${1:?Provide file name as first parameter please}

run_both "${FILE}"
