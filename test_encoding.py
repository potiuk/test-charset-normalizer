#!python
import chardet
import charset_normalizer
import requests
import csv
import re
import warnings
import tqdm
import sys

client = requests.Session()
results = []
charset_regex = re.compile("charset=([^;]+)")

# Charset_normalizer warns if the data contains encoding information
warnings.filterwarnings('ignore', 'Trying to detect')

prefix = sys.argv[1]
with open(prefix, 'r') as fp:
    data = fp.readlines()

skipped = 0
no_encoding = 0
done = 0
exception = 0

for row in data:
    # Change value if urls are not in the second column
    url = row.strip()
    print("Trying url '{0}'".format(url))
    try:
        response = client.get("https://{0}".format(url), timeout=2)
    except:
        print("\tFailed https, trying http")
        try:
            response = client.get("http://{0}".format(url), timeout=2)
        except:
            print("\tFailed http, skipping")
            skipped += 1
            continue
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
    chardet_encoding = chardet.detect(response.content)
    try:
        normalizer_encoding = charset_normalizer.detect(response.content)
    except Exception as e:
        exception += 1
    results.append([url, declared_encoding, chardet_encoding['encoding'], normalizer_encoding['encoding']])

with open(f'res/{prefix}_summary.txt', 'w') as fp:
    fp.write("{0}, {1}, {2}, {3}\n".format(done, skipped, no_encoding, exception))

print("Run finished, resolved {0} urls successfully, skipped {1}. {2} "
      "reported no encoding scheme, {3} exceptions".format(
    done, skipped, no_encoding, exception))

with open(f'res/{prefix}_all_results.csv', 'w') as fp:
    writer = csv.writer(fp)
    writer.writerows(results)

with open(f'res/{prefix}_differences.md', 'w') as fp:
    for row in results:
        if row[1] is None:
            fp.write("| {0} | {1} | {2} |\n".format(row[0], row[2], row[3]))
