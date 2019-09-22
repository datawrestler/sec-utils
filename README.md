[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


#### Welcome to bulkedgar
Batch SEC Downloader is a utility package to facilitate large bulk downloads of SEC documents. It works with any SEC document type and will retrieve the entire historical database if required. It downloads SEC documents over multiple threads. 

- [Motivation](#motivate)
- [Installation](#install)
- [Usage](#usage)

##### Motivation <a id='motivate' />
Bulk SEC Downloader picks up where a number of other repos left off. There are a couple SEC downloading python packages out there, however they are designed from retrieval of few documents. I needed a way to consistently download the latest updates from the SEC and secure a local copy of the entire history of the SEC. This translates into TB's of documents, where fundamentally different issues arise like networking issues, storage issues, etc. 

There is a nice package available to download and construct index files, however the user is still left to download the actual files and must be comfortable with bash scripting. 

With bulk-python-edgar the program handles files you have already retrieved, get's the missing files you don't have in your local archive, and continues. 

For examples of other repos that exist: 

- [sec-edgar-downloader](https://github.com/jadchaar/sec-edgar-downloader)
- [python-edgar](https://github.com/edouardswiac/python-edgar/)

Furthermore, the hope of this package is to create parsers for repsective form types. A user could import the 10-K parser and call the Management Discussion and Analysis method to retrieve respective MD&A's from selected files. 

There are also plans to integrate directly with popular cloud providers given the scale of these filings. Processing 10-K/Q's alone requires TB's of storage.

##### Installation <a id='install' />
Installation can be done straight from source or the python packaging index:

```bash
pip install bulkedgar
```

##### Usage <a id='usage' />
```bash
python download_sec.py --output_dir=/mnt/sda/sec --form_types=S-1 --num_workers=-1 --start_year=2014 --end_year=2019 --quarters 1 2 3 4
```

Additionally, users can leverage the API directly for more hands on work:
```python
from bulkedgar import FormIDX
form = FormIDX(year=2017, quarter=1, seen_files=None, cache_dir=None, form_types=['10-K])
files = form.index_to_files()
form.master_index.head()
# CIK	Company Name	Form Type	Date Filed	Filename	fname
# 1000015	META GROUP INC	10-K	1998-03-31	edgar/data/1000015/0001000015-98-000009.txt	0001000015-98-000009.txt
# 1000112	CHEVY CHASE MASTER CREDIT CARD TRUST II	10-K	1998-03-27	edgar/data/1000112/0000920628-98-000038.txt	0000920628-98-000038.txt
# 1000179	PARAMOUNT FINANCIAL CORP	10-K	1998-03-30	edgar/data/1000179/0000950120-98-000108.txt	0000950120-98-000108.txt

# you can download individual files:
files[0].download_file(output_directory)
```

