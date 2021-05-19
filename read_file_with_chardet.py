#!/usr/bin/env python
import chardet
import sys

from timebudget import timebudget


@timebudget
def detect(data_to_detect: bytes):
    return chardet.detect(data)


@timebudget
def read_file():
    file = sys.argv[1]
    with open(file, 'rb') as fp:
        return fp.read()



data=read_file()
chardet_result = detect(data)
