#!/bin/bash

# example bash script to kick off long running download run

# source environment w/secutils installed
source /home/datawrestler/anaconda3/bin/activate sec_env

# PARAMETERS
OUTPUT_DIR=/home/datawrestler/data/sec
CACHE_DIR=/home/datawrestler/data/sec/cache

python -m secutils.download_sec \
    --output_dir=$OUTPUT_DIR \
    --form_types "DEF 14A" "DEFA14A" \
    --num_workers=-1 \
    --start_year=2009 \
    --end_year=2020 \
    --quarters 1 2 3 4 \
    --cache_dir=$CACHE_DIR