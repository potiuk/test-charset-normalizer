# Context: Why comparing chardet and charset-normalizer?

This is an experiment to compare results of `chardet` and `charset-normalizer`. The `chardet` package is
currently (13 May 2020) a mandatory dependency of `requests` and since `chardet` is LGPL, it makes it
impossible to be used in the Apache Software Foundation projects as mandatory dependency. Since
`requests` is currently 3rd most-popular package used in PyPI, this excludes a lot of pacakges
from being used in the Apache Software Foundation projects. Therefore a group of Apache Airflow PMC members
attempted to convince `requests` maintainers to switch to a `charset-normalizer` which is on MIT
dependency and seems to provide very similar functionality.

Hopefully results of the tests performed and resulting fixes to `charset-normalizer` will make it appealing
for the `requests` maintainer to switch to it.

# Compare chardet and charset-normalizer with 33K sites vs. chardet

This repository allows performs comparison between results of ~33.000 main pages of sites (the top 1000 sites
from 80  countries in the world according to [Data for SEO](https://dataforseo.com/top-1000-websites).

In order to run the comparison you need to:

* create and switch to virtualenv using requirements.txt
* have `GNU Parallel` installed
* have a decently Powerful machine to run it on (the run runs by default 34 processes reading and running
  detection on the content from 30K sites, and they keep 16 core CPU busy for > 1 h)
* run `./run_site_comparision.sh`

# Test Charset-normalizer performance vs chardet 

Another area identified by @nateprewitt in
[this comment](https://github.com/psf/requests/pull/5797#issuecomment-842939345)
was the area of performance on big files.

Chardet seems to do much better on non-space delimited big files. The tests here generate different
kinds of big files (TODO) and run comparative performance for both elapsed time and memory (TODO) of
processing for both  chardet and charset normalizer.


## Prerequisites

* numfmt

## Running

* Run `./generate_all_files.sh` -> generates all files in "big_files" folder
* Run comparison for selected file:
   `./run_file_system_comparision.sh big_files/<FILE_NAME>`


# More information

* [Charset-normalizer PR to requests](https://github.com/psf/requests/pull/5797)
* [Discussion in Apache Software Foundation's JIRA](https://issues.apache.org/jira/browse/LEGAL-572)

# Credits

* The PR to implement Charset was done by @ashb.
* The original version of the test written by @da1910 and tested on 500 top Alexa sites.
* @Ousret for super speedy diagnosis and fixes in charset-normalizer.
* @sigmavirus24 for understanding the needs of the users and looking into it despite feature-freeze of `requests`

# This repo content

* [URLS.csv](URLS.csv) - list of `33138` top sites from `80` countries in the world
* The x* - the URLS.csv - split into smaller chunks
* res/ - results of the test (per chunks and combined)
   * `all` - all URLS tested
   * `different` - different encodings returned by chardet/charset-normalizer
   * `same` - same encodings returned by chardet/charset-normalizer
   * `exceptions.txt` - exception caught during charset-normalizer processing
   * `summary.txt` - summary counts (processed urls, skipped urls, urls without encoding, exceptions)

# Results

# Compatibility with chardet when it comes to encoding

We've already identified and the super-responsive @Ousret fixed several bugs and
in `charset-normalizer` thanks to the tests performed:

* [:bug: Legacy detect should return UTF-8-SIG if sig is detected](https://github.com/Ousret/charset_normalizer/pull/38)
* [:bug: Fix empty payload detection/alphabets listing](https://github.com/Ousret/charset_normalizer/pull/39)
* [:bug: Fix very rare case of ?bad? characters that cannot be translated to Unicode](https://github.com/Ousret/charset_normalizer/pull/40)

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


TODO: add results for the tests


# Additional changes to charset-normalizer

* The following areas were also identified by @nateprewitt in
  [this comment](https://github.com/psf/requests/pull/5797#issuecomment-842939345) and they 
  were addressed by @Ousret in the TODO: version of `charset-normalizer`:
  * default to ascii character set if in doubt
  * decrease a number of dependencies of `charset-normalizer`
