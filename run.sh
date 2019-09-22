#!/bin/bash

source /home/datawrestler/anaconda3/bin/activate sec_env

python download_sec.py \
    --output_dir=/mnt/sda/sec \
    --form_types S-1 S-1/A \
    --num_workers=-1 \
    --start_year=1995 \
    --end_year=2019 \
    --quarters 1 2 3 4 \
    --cache_dir=/mnt/sda/sec/cache