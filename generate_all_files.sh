#!/usr/bin/env bash
set -euo pipefail

# Generate files with repeated "test", no lines no spaces

./generate_file.sh 10 "test" big_files/test-4K.txt
./generate_file.sh 22 "test" big_files/test-16MB.txt
./generate_file.sh 23 "test" big_files/test-32MB.txt
./generate_file.sh 24 "test" big_files/test-64MB.txt
./generate_file.sh 25 "test" big_files/test-128MB.txt
./generate_file.sh 26 "test" big_files/test-256MB.txt
./generate_file.sh 27 "test" big_files/test-512MB.txt
./generate_file.sh 28 "test" big_files/test-1GB.txt
./generate_file.sh 29 "test" big_files/test-2GB.txt
