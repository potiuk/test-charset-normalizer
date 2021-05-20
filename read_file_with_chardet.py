#!/usr/bin/env python
import chardet
import sys

from timebudget import timebudget


@timebudget
def detect(data_to_detect: bytes):
    return chardet.detect(data_to_detect)


# noinspection DuplicatedCode
@timebudget
def read_file():
    file = sys.argv[1]
    with open(file, 'rb') as fp:
        return fp.read()


def main():
    data = read_file()
    chardet_result = detect(data)


if __name__ == '__main__':
    main()
