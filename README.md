[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/datawrestler/sec-utils.svg?branch=master)](https://travis-ci.org/datawrestler/sec-utils)

#### Welcome to bulkedgar
Batch SEC Downloader is a utility package to facilitate large bulk downloads of SEC documents. It works with any SEC document type and will retrieve the entire historical database if required. It downloads SEC documents over multiple threads.

Key functionality includes:
- Multi-threaded downloading
- Caching of index files
- Automatic directory structure buildout (i.e. downloading multiple file types w/dir structure: ftype --> year --> quarter --> files)
- Resume downloading
- Built in logging and download success tracker

Overview of README:
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
There are two primary methods of installing sec-utils. The first is via the python packaging index (pypi). The second is straight from source. 

To install from pypi:
```bash
pip install secutils
```

And to install from source:
```bash
git clone https://github.com/datawrestler/sec-utils && cd sec-utils
conda create --name sec_env python=3.7 pip
conda activate sec_env
pip install -r requirements.txt
pip install -e .
```

##### Usage <a id='usage' />
```bash
python download_sec.py --output_dir=/mnt/sda/sec --form_types=S-1 --num_workers=-1 --start_year=2014 --end_year=2019 --quarters 1 2 3 4
```
Even more cleanly, you can coordinate long running jobs and keep track of your parameters by modifying this [example script](https://github.com/datawrestler/sec-utils/blob/master/examples/run.sh)

Make sure to make it executable on your system:
```bash
chmod +x run.sh
./run.sh
```

Additionally, users can leverage the API directly for more hands on work:
```python
from secutils.edgar import FormIDX
form = FormIDX(year=2017, quarter=1, seen_files=None, cache_dir=None, form_types=['10-K])
files = form.index_to_files()
form.master_index.head()
# CIK	Company Name	Form Type	Date Filed	Filename	fname
# 1000015	META GROUP INC	10-K	1998-03-31	edgar/data/1000015/0001000015-98-000009.txt	0001000015-98-000009.txt
# 1000112	CHEVY CHASE MASTER CREDIT CARD TRUST II	10-K	1998-03-27	edgar/data/1000112/0000920628-98-000038.txt	0000920628-98-000038.txt
# 1000179	PARAMOUNT FINANCIAL CORP	10-K	1998-03-30	edgar/data/1000179/0000950120-98-000108.txt	0000950120-98-000108.txt

# lets take a peek at attributes available to individual files:
ex = files[0]
msg = f"""
      Company Name: {ex.company_name}
      CIK Number: {ex.cik_number}
      Date Filed: {ex.date_filed}
      Form Type: {ex.form_type}
      File Name: {ex.file_name}
      Download URL: {ex.file_download_url}
      """
print(msg) 
# Company Name: OPTICAL CABLE CORP
# CIK Number: 1000230
# Date Filed: 2017-12-20 00:00:00
# Form Type: 10-K
# File Name: 0001437749-17-020936.txt
# Download URL: https://www.sec.gov/Archives/edgar/data/1000230/0001437749-17-020936.txt                                                                        
# get example file and download:
# to download our example file:
output_dir = '.'
ex.download_file(output_dir) # 200 is a successful download

# verify download 
import os
list(filter(lambda x: x.endswith('txt'), os.listdir(output_dir)))
# ['0001437749-17-020936.txt']
```

Getting hands on is great, however using the CLI does provide several advantages:
- Automatic directory structure creation
- Built in logging and caching
- Ability to resume training via download scanning
- Multi-threaded file downloading