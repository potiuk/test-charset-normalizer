#!/usr/bin/env python
import os
import traceback
from typing import NamedTuple, Optional

import chardet
import charset_normalizer
import click
import requests
import csv
import re
import warnings
import sys

from rich.console import Console
console = Console(color_system="256", width=400)

client = requests.Session()
results = []
charset_regex = re.compile("charset=([^;]+)")

# Charset_normalizer warns if the data contains encoding information
warnings.filterwarnings('ignore', 'Trying to detect')


class Result(NamedTuple):
    url: str
    declared_encoding: Optional[str]
    chardet_encoding: str
    normalizer_encoding: str


def compare_encodings(encoding1: str, encoding2: str):
    if encoding1 is None and encoding2 is None:
        # When both report none, they match
        return True
    if encoding1 is None or encoding2 is None:
        # but if only one, they don't
        return False
    # otherwise compare it adjusting to case/underscore/hyphen equivalence
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    return encoding1.upper().replace("_", "-") == encoding2.upper().replace("_", "-")


@click.group(invoke_without_command=True)
@click.option("--input-directory", type=str, required=True, help="Directory where to read input file from")
@click.option("--output-directory", type=str, required=True, help="Directory where to store results to")
@click.argument('prefix', nargs=1)
def main(input_directory: str, output_directory: str,  prefix: str):
    with open(os.path.join(input_directory, prefix), 'r') as fp:
        data = fp.readlines()

    skipped = 0
    no_encoding = 0
    done = 0
    exceptions = 0

    with open(f'{output_directory}/{prefix}_same.md', 'w') as same, \
            open(os.path.join(output_directory, f'{prefix}_different.md'), 'w') as different, \
            open(os.path.join(output_directory, f'{prefix}_all.csv'), 'w') as all_succeeded, \
            open(os.path.join(output_directory, f'{prefix}_skipped.csv'), 'w') as all_skipped, \
            open(os.path.join(output_directory, f'{prefix}_exceptions.txt'), 'w') as all_exceptions:
        all_skipped_writer = csv.writer(all_skipped)
        all_succeeded_writer = csv.writer(all_succeeded)

        for i, row in enumerate(data):
            # Change value if urls are not in the second column
            url = row.strip()
            console.print(f"[{int(i/len(data)*1000)/10:.1f}%]Trying url '{url}'", end='')
            # noinspection PyBroadException
            try:
                response = client.get("https://{0}".format(url), timeout=2)
                console.print('\t[green]Succeeded[/]')
            except Exception as https_exception:
                first_line = str(https_exception).splitlines(keepends=False)[0][:70]
                console.print(f"\t[blue]Failed https: {first_line}]", end="")
                # noinspection PyBroadException
                try:
                    response = client.get("http://{0}".format(url), timeout=2)
                except Exception as http_exception:
                    first_line = str(https_exception).splitlines(keepends=False)[0][:70]
                    console.print(f"\t[yellow]Failed http: {first_line}, skipping[/]")
                    skipped += 1
                    all_skipped_writer.writerow([url, str(https_exception), str(http_exception)])
                    continue
                console.print('\t[green]Succeeded[/]')
            done += 1
            if 'Content-Type' in response.headers and 'charset' in response.headers['Content-Type']:
                content_header = response.headers['Content-Type']
                header = charset_regex.search(content_header)
                if header:
                    declared_encoding = header.group(1)
                else:
                    no_encoding += 1
                    declared_encoding = None
            else:
                no_encoding += 1
                declared_encoding = None
            chardet_result = chardet.detect(response.content)
            # noinspection PyBroadException
            try:
                normalizer_result = charset_normalizer.detect(response.content)
                result = Result(url=url,
                                declared_encoding=declared_encoding,
                                chardet_encoding=chardet_result['encoding'],
                                normalizer_encoding=normalizer_result['encoding'])
                if result.declared_encoding is None:
                    if compare_encodings(result.chardet_encoding, result.normalizer_encoding):
                        same.write("| {0} | {1} | {2} |\n".format(result.url,
                                                                  result.chardet_encoding,
                                                                  result.normalizer_encoding))
                        same.flush()
                    else:
                        different.write("| {0} | {1} | {2} |\n".format(result.url,
                                                                       result.chardet_encoding,
                                                                       result.normalizer_encoding))
                        different.flush()
                all_succeeded_writer.writerow(result)

            except Exception as e:
                exceptions += 1
                console.print(f"[red]Exception when processing {url}[/]")
                traceback.print_exc()
                print(f"Exception when processing {url}", file=all_exceptions)
                print("#" * 80, file=all_exceptions)
                traceback.print_exc(file=all_exceptions)
                print("#" * 80, file=all_exceptions)
                all_exceptions.flush()

        console.print("#" * 80)
        console.print("Run finished, resolved {0} urls successfully, skipped {1}. {2} "
                      "reported no encoding scheme, {3} exceptions".format(done, skipped, no_encoding, exceptions))
        console.print("#" * 80)

    with open(f'res/{prefix}_summary.csv', 'w') as summary:
        summary.write("{0}, {1}, {2}, {3}\n".format(done, skipped, no_encoding, exceptions))


if __name__ == '__main__':
    main()
