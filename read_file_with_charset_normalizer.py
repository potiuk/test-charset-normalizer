#!/usr/bin/env python
import warnings
import sys

from timebudget import timebudget

# Charset_normalizer warns if the data contains encoding information
from charset_normalizer import CharsetNormalizerMatches as CnM

warnings.filterwarnings('ignore', 'Trying to detect')


@timebudget
def detect(data_to_detect: bytes):
    return CnM.from_bytes(
        data_to_detect,
        steps=10,  # Number of steps/block to extract from my_byte_str
        chunk_size=10240,  # Set block size of each extraction
        threshold=0.2,  # Maximum amount of chaos allowed on first pass
        preemptive_behaviour=False,  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
        explain=False  # Print on screen what is happening when searching for a match
    )


@timebudget
def read_file():
    file = sys.argv[1]
    with open(file, 'rb') as fp:
        return fp.read()


data = read_file()
charset_normalizer_result = detect(data)
