# Context: Why comparing chardet and charset-normalizer?

This is an experiment to compare results of `chardet` and `charset-normalizer`. The `chardet` package is
currently (20th of May 2021) a mandatory dependency of `requests` and since `chardet` is `LGPL`, it makes it
impossible to be used in the Apache Software Foundation projects as mandatory dependency.

Since `requests` is currently 3rd most-popular package used in PyPI, this excludes a lot of packages
from being used in the Apache Software Foundation projects. A group of Apache Airflow PMC members
attempted to convince `requests` maintainers to switch to a `charset-normalizer` which is on MIT
dependency and seems to provide very similar functionality. The `charset-normalizer` author
[@Ousret](https://github.com/Ourset) helps to get it there.

Hopefully results of the tests performed and resulting fixes to `charset-normalizer` will make it appealing
for the `requests` maintainer to switch to it.

# Comparing encoding vs. chardet

The test performs comparison between results of ~33.000 main pages of sites (the top 1000 sites
from 80  countries in the world according to [Data for SEO](https://dataforseo.com/top-1000-websites).

## Prerequisites

* venv with dependencies from `requirements.txt`
* ``GNU Parallel``

## Running Encoding comparisions 

In order to run the comparison you need to:

* create and switch to virtualenv using requirements.txt
* have `GNU Parallel` installed
* have a decently Powerful machine to run it on (the run runs by default 34 processes reading and running
  detection on the content from 30K sites, and they keep 16 core CPU busy for > 1 h)
* run `./run_site_comparision.sh`

# Comparing performance vs. chardet 

The tests here generate different kinds of big files  and run comparative performance for both elapsed
time and memory of processing for both  chardet and charset normalizer.

## Prerequisites

* venv with dependencies from `requirements.txt`
* ``numfmt``

## Running performance tests

* Run `./generate_all_files.sh` -> generates all files in "big_files" folder
* Run comparison for selected file:
   `./run_file_system_comparision.sh big_files/<FILE_NAME>`
  
# More information

* [Charset-normalizer PR to requests](https://github.com/psf/requests/pull/5797)
* [Discussion in Apache Software Foundation's JIRA](https://issues.apache.org/jira/browse/LEGAL-572)

# Credits

* The PR to implement Charset was done by [@ashb](https://github.com/ashb).
* The original version of the test written by [@da191](https://github.com/da191) and tested on 500 top Alexa sites.
* [@sigmavirus24](https://github.com/sigmavirus24) for understanding the needs of the users and looking into it despite feature-freeze of `requests`
* [@ntaeprewitt](https://github.com/nateprewitt) for caring about performance, large files and fallback behaviour
* Special thanks to [@Ousret](https://github.com/Ourset) for super-speedy diagnosis and fixes in charset-normalizer with < 1day turnaround.

# Encoding test files

* [URLS.csv](URLS.csv) - list of `33138` top sites from `80` countries in the world
* The `URLS-split/x*` - the URLS.csv split into smaller chunks to paralellize the work
* `res/` - results of the encoding comparision tests (per chunks and combined)
   * `all` - all URLS tested
   * `different` - different encodings returned by chardet/charset-normalizer
   * `same` - same encodings returned by chardet/charset-normalizer
   * `exceptions.txt` - exception caught during charset-normalizer processing
   * `summary.txt` - summary counts (processed urls, skipped urls, urls without encoding, exceptions)

# Performance test files

* `big_files` - here big files are stored

# Compatibility with chardet when it comes to encoding

We've already identified, and the super-responsive @Ousret fixed several bugs and
in `charset-normalizer` thanks to the tests performed:

* [:bug: Legacy detect should return UTF-8-SIG if sig is detected](https://github.com/Ousret/charset_normalizer/pull/38)
* [:bug: Fix empty payload detection/alphabets listing](https://github.com/Ousret/charset_normalizer/pull/39)
* [:bug: Fix very rare case of ?bad? characters that cannot be translated to Unicode](https://github.com/Ousret/charset_normalizer/pull/40)
* [Improved dependencies/performance/fallback behaviou ](https://github.com/Ousret/charset_normalizer/pull/41)

# Performance tests results comparing to chardet

Preliminary results:

# 19.05.2021 (charset-normalizer 1.3.9)

   Seems that processing big files is the weak point of charset-normalizer. Both chardet and
   charset-normalizer processing time is proportional to the amount of data in the content, 
   but `charset-normalizer` is roughly 20x slower than chardet.

| Size  | Reading file | Chardet detection | Charset-normalizer detection |
|-------|--------------|-------------------|------------------------------|
| 16MB  | 5.5ms        | 0.17s             | 2.92s                        |
| 32MB  | 11ms         | 0.32s             | 6.46s                        |
| 64MB  | 22ms         | 0.64s             | 12.9s                        |
| 128MB | 44ms         | 1.3s              | 25.6s                        |
| 256MB | 88ms         | 2.6s              | 50.8s                        |


Changing the parameters did not seem to have significant impact on the timing

```
    return CnM.from_bytes(
        data_to_detect,
        steps=10,  # Number of steps/block to extract from my_byte_str
        chunk_size=512,  # Set block size of each extraction
        threshold=0.2,  # Maximum amount of chaos allowed on first pass
        preemptive_behaviour=False,  # Determine if we should look into my_byte_str (ASCII-Mode) for pre-defined encoding
        explain=False  # Print on screen what is happening when searching for a match
    )
```


# 21.05.2021 (charset-normalizer 1.4.0 candidate)

* Encoding comparision: no exception, 83% match on no-encoding sites chardet vs. charset normalizer
* Performance comparision

Seems that Chardet does very good on simple content. After some improvements in 1.4.0 candidate
the difference for Charset vs. Charset normalizer for ASCII only files decreased to ~10x from ~20x
(tests performed on a different machine):

| Size  | Reading file | Chardet detection | Charset-normalizer detection |
|-------|--------------|-------------------|------------------------------|
| 16MB  | 4.5ms        | 0.20s             | 1.9s                         |
| 32MB  | 8ms          | 0.45s             | 3.17s                        |
| 64MB  | 14ms         | 0.91s             | 7.32s                        |
| 128MB | 27ms         | 1.8s              | 14.7s                        |
| 256MB | 51ms         | 3.6s              | 28.6s                        |

However, things get more interesting when the files contain actual encoded
characters other than only ASCII characters. Seems that chardet-normalizer is
able to decode even big files but chardet performs very poor on big files
containing non-ASCII characters.

Processing time of chardet seems in this case proportional to the size of the data
and in case of charset-normalized it is much less linearly depending on the
size. In both cases below the size where charset-normalizer starts to
be faster than chardet is between 32K and 64K of data.

Detecting Polish characters:

| Size  | Reading file | Chardet detection | Charset-normalizer detection |
|-------|--------------|-------------------|------------------------------|
| 4K    | 0.027ms      | 0.05s             | 0.28s                        |
| 8K    | 0.036ms      | 0.17s             | 0.52s                        |
| 16K   | 0.032ms      | 0.18s             | 0.54s                        |
| 32K   | 0.039ms      | 0.35s             | 0.29s                        |
| 64K   | 0.075ms      | 0.7s              | 0.68s                        |
| 128K  | 0.087ms      | 1.4s              | 0.68s                        |
| 256K  | 0.153ms      | 2.78s             | 0.57s                        |
| 512K  | 0.242ms      | 5.63s             | 0.34s                        |
| 1MB   | 0.470ms      | 11.2s             | 0.77s                        |
| 2MB   | 0.942ms      | 22.2s             | 1.38s                        |
| 4MB   | 1.45ms       | 45s               | 0.93s                        |
| 8MB   | 2.39ms       | 90s               | 1.08s                        |
| 16MB  | 4ms          | 180s              | 0.85s                        |
| 32MB  | 8ms          | - >>3m            | 3.17s                        |
| 64MB  | 14ms         | - >>3m            | 7.32s                        |
| 128MB | 27ms         | - >>3m            | 14.7s                        |
| 256MB | 51ms         | - >>3m            | 28.6s                        |

Detecting Japanese characters:


| Size  | Reading file | Chardet detection | Charset-normalizer detection |
|-------|--------------|-------------------|------------------------------|
| 4K    | 0.03ms       | 0.06s             | 0.32s                        |
| 8K    | 0.03ms       | 0.23s             | 0.63s                        |
| 16K   | 0.04ms       | 0.25s             | 0.63s                        |
| 32K   | 0.04ms       | 0.49s             | 0.35s                        |
| 64K   | 0.07ms       | 0.98s             | 0.78s                        |
| 128K  | 0.09ms       | 1.97s             | 0.77s                        |
| 256K  | 0.15ms       | 3.97s             | 0.65s                        |
| 512K  | 0.27ms       | 7.8s              | 0.67s                        |
| 1MB   | 0.59ms       | 15.5s             | 0.89s                        |
| 2MB   | 0.95ms       | 31.3s             | 1.01s                        |
| 4MB   | 1.53ms       | 63s               | 1.10s                        |
| 8MB   | 2.3ms        | 240s              | 1.27s                        |
| 16MB  | 4ms          | - >>3m            | 1.26s                        |
| 32MB  | 8ms          | - >>3m            | 1.75s                        |
| 64MB  | 14ms         | - >>3m            | 5.46s                        |
| 128MB | 25ms         | - >>3m            | 4.10s                        |
| 256MB | 49ms         | - >>3m            | 8.2s                         |


# 05.07.2021 (charset-normalizer 2.0.0)

Summary: charset-normalizer became really fast

ASCII characters:

| Size   | Chardet | Charset_normalizer |
|--------|---------|--------------------|
| 4K     | 0.007 s | 0.018s             |
| 16MB   | 0.165 s | 0.019s             |
| 32MB   | 0.332 s | 0.019 s            |
| 64MB   | 0.648 s | 0.010 s            |
| 128MB  | 1.293 s | 0.005 s            |
| 256MB  | 2.579 s | 0.018 s            |

Polish characters:

| Size | Chardet  | Charset_normalizer |
|------|----------|--------------------|
| 4K   | 0.027s   | 0.053s             |
| 8K   | 0.054s   | 0.069s             |
| 16K  | 0.106s   | 0.074s             |
| 32K  | 0.213s   | 0.057s             |
| 64K  | 0.453s   | 0.086s             |
| 128K | 0.847s   | 0.089s             |
| 256K | 1.697s   | 0.089s             |
| 512K | 3.416s   | 0.094s             |
| 16MB | 110s (!) | 0.272s             |


Japanese characters:

| Size | Chardet  | Charset_normalizer |
|------|----------|--------------------|
| 4K   | 0.037s   | 0.172s             |
| 8K   | 0.074s   | 0.317s             |
| 16K  | 0.147s   | 0.314s             |
| 32K  | 0.290s   | 0.179s             |
| 64K  | 0.577s   | 0.399s             |
| 128K | 1.178s   | 0.448s             |
| 256K | 2.359s   | 0.389s             |
| 512K | 4.699s   | 0.324s             |
| 16MB | 150s (!) | 0.848s             |

