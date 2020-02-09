import os
import logging
import httplib2
import argparse
from pathlib import Path
from itertools import product
from datetime import datetime
import multiprocessing
from typing import List

from tqdm.auto import tqdm

from secutils.edgar import FormIDX, SECContainer, DocumentDownloaderThread
from secutils.utils import scan_output_dir, _read_cik_config, yaml_config_to_args

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=Path, default=None, help='default download path')
    parser.add_argument('--form_types', nargs='+', default=None, help='form types to download')
    parser.add_argument('--num_workers', default=-1, type=int, help='Number of download workers')
    parser.add_argument('--start_year', type=int, help='Download start year')
    parser.add_argument('--end_year', type=int, help='Download end year')
    parser.add_argument('--quarters', default=-1, nargs='+', type=int, choices=[-1, 1, 2, 3, 4], 
                        help='Quarters of documents to download - if -1 then all quarters')
    parser.add_argument('--log_level', default='INFO', choices=['INFO', 'ERROR', 'WARN'], help='Default logging level')
    parser.add_argument('--cache_dir', type=str, help='form idx cache dir')
    parser.add_argument('--ciks', nargs='+', type=int, help='List of CIKs to download')
    parser.add_argument('--cik_path', type=str, help='Path to CIK text file')
    parser.add_argument('--config_path', type=str, help='Path to yml config file')
    args = parser.parse_args()

    if args.config_path:
        args = yaml_config_to_args(args)

    if args.quarters == -1:
        args.quarters = list(range(1, 5))

    if args.cik_path:
        args.ciks = _read_cik_config(args.cik_path)

    # Setup logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=getattr(logging, args.log_level))

    if args.num_workers == -1:
        args.num_workers = multiprocessing.cpu_count()

    # init container
    sec_container = SECContainer()
    sec_container.to_visit = set()
    sec_container.downloaded = set()
    sec_container.download_error = set()
    sec_container.last_url_message = '200'
    # capture seen files to filter out of new files
    seen_files = scan_output_dir(args.output_dir)
    logger.info(f'Scanned output dir - located {len(seen_files)} downloaded files')
    # iterator of years/quarters
    years = list(range(args.start_year, args.end_year+1))
    time = list(product(years, args.quarters))
    for (yr, qtr) in tqdm(time, total=len(time)):
        sec_container.year = yr
        sec_container.quarter = qtr
        logger.info(f'Downloading files - Year: {yr} - Quarter: {qtr}')
        files = FormIDX(year=yr, quarter=qtr, seen_files=seen_files, cache_dir=args.cache_dir, 
               form_types=args.form_types, ciks=args.ciks).index_to_files()
        if len(files) > 0:
            sec_container.to_visit.update(files)
            with tqdm(total=len(sec_container.to_visit), desc=f"Downloading: Year: {yr} - Quarter: {qtr}") as pbar:
                # create threads and distribute downloads
                sec_container.pbar = pbar
                logger.info(f'Creating {args.num_workers} download threads')
                threads = [DocumentDownloaderThread(i, f'thread-{i}', args.output_dir, args.cache_dir) for i in range(args.num_workers)]
                # start threads
                [thread.start() for thread in threads]
                # delay execution of remaining script until all threads complete
                [thread.join() for thread in threads]


if __name__ == '__main__':
    main()