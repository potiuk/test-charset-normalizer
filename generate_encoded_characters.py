#!/usr/bin/env python
import sys

import click

ENCODINGS = {
    "Windows-1250": "zażółć gęśląjaźń",
    "SHIFT_JIS": "7ビット及び8ビッ",
}


@click.group(invoke_without_command=True)
@click.option("--encoding", type=str, required=True, help="Encoding to print characters in")
def main(encoding: str):
    characters = ENCODINGS[encoding]
    encoded_characters = characters.encode(encoding)
    length = len(encoded_characters)
    if length != 16:
        raise Exception(f"The encoded characters length ({length}) should be 16 bytes exactly!")
    sys.stdout.buffer.write(encoded_characters)


if __name__ == '__main__':
    main()
