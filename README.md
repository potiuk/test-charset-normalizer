# Compare chardet and charset-normalizer

This is an experiment to compare results of `chardet` and `charset-normalizer`. The `chardet` package is
currently (13 May 2020) a mandatory dependency of `requests` and since `chardet` is LGPL, it makes it
impossible to be used in the Apache Software Foundation projects as mandatory dependency. Since
`requests` is currently 3rd most-popular package used in PyPI, this excludes a lot of pacakges
from being used in the Apache Software Foundation projects. Therefore a group of Apache Airflow PMC members
attempted to convince `requests` maintainers to switch to a `charset-normalizer` which is on MIT
dependency and seems to provide very similar functionality.

Hopefully results of the tests performed and resulting fixes to `charset-normalizer` will make it appealing
for the `requests` maintainer to switch to it.

We've already identified and the super-responsive @Ousret fixed several bugs and
in `charset-normalizer` thanks to the tests performed:

* [:bug: Legacy detect should return UTF-8-SIG if sig is detected](https://github.com/Ousret/charset_normalizer/pull/38)
* [:bug: Fix empty payload detection/alphabets listing](https://github.com/Ousret/charset_normalizer/pull/39)
* [:bug: Fix very rare case of ?bad? characters that cannot be translated to Unicode](https://github.com/Ousret/charset_normalizer/pull/40)

This repository allows performs comparison between results of ~33.000 main pages of sites (the top 1000 sites
from 80  countries in the world according to [Data for SEO](https://dataforseo.com/top-1000-websites). 

In order to run the comparison you need to:

* create and switch to virtualenv using requirements.txt
* have `GNU Parallel` installed
* have a decently Powerful machine to run it on (the run runs by default 34 processes reading and running
  detection on the content from 30K sites, and they keep 16 core CPU busy for > 1 h)  
* run `./run_test.sh`

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
