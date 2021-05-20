#!/usr/bin/env bash
set -euo pipefail

# Generate files with repeated "test", no lines no spaces

function generate_various_sizes() {
    ./generate_file.sh 8 "${1}" big_files/"${2}"-4K.txt
    ./generate_file.sh 20 "${1}" big_files/"${2}"-16MB.txt
    ./generate_file.sh 21 "${1}" big_files/"${2}"-32MB.txt
    ./generate_file.sh 22 "${1}" big_files/"${2}"-64MB.txt
    ./generate_file.sh 23 "${1}" big_files/"${2}"-128MB.txt
    ./generate_file.sh 24 "${1}" big_files/"${2}"-256MB.txt
    ./generate_file.sh 25 "${1}" big_files/"${2}"-512MB.txt
    ./generate_file.sh 26 "${1}" big_files/"${2}"-1GB.txt
    ./generate_file.sh 27 "${1}" big_files/"${2}"-2GB.txt
}

# all probes should have 16 bytes !
generate_various_sizes "testtesttesttest" "test"
# generate_various_sizes "$(./generate_encoded_characters.p --encoding "Windows-1250")" "pl"
# generate_various_sizes "$(./generate_encoded_characters.p --encoding "SHIFT_JIS")" "jp"
