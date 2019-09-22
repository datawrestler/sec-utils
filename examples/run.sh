#!/bin/bash

# example bash script to kick off long running download run

# source environment w/secutils installed
source /home/datawrestler/anaconda3/bin/activate sec_env

# PARAMETERS
OUTPUT_DIR=/mnt/sda/sec
CACHE_DIR=/mnt/sda/sec/cache

python -m secutils.download_sec \
    --output_dir=$OUTPUT_DIR \
    --form_types S-1 S-1/A \
    --num_workers=-1 \
    --start_year=1995 \
    --end_year=2019 \
    --quarters 1 2 3 4 \
    --cache_dir=$CACHE_DIR