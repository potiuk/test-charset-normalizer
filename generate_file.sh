#!/usr/bin/env bash
set -euo pipefail

# size of file = len(CONTENT) * 2 ^ NUM_LOOPS
NUM_LOOPS="${1?:Missing number of loops as first parameter}"
# The content is repeated
CONTENT="${2?:Missing content as second parameter}"
# file name
FILENAME=${3?:Missing filename as third parameter}

CONTENT_LENGTH=${#CONTENT}

echo "Creating file of the size of $(numfmt --to=iec $(( CONTENT_LENGTH * 2 ** NUM_LOOPS)))B"

echo -n "${CONTENT}" > "${FILENAME}"

for loop in $(seq 1 "${NUM_LOOPS}")
do
    echo -n "."
    # shellcheck disable=SC2094
    cp "${FILENAME}" "${FILENAME}.tmp"
    mv "${FILENAME}" "${FILENAME}.tmp2"
    cat "${FILENAME}.tmp" "${FILENAME}.tmp2" > "${FILENAME}"
    rm "${FILENAME}.tmp" "${FILENAME}.tmp2"
done

echo
