import os
import argparse
from pathlib import Path
from typing import Union, List, Optional
from datetime import datetime

import ftfy
import yaml


def generate_config(fpath: Optional[str]=None) -> str:
    """generate sample config file"""

    if not fpath:
        fpath = os.getcwd()

    full_fpath = os.path.join(fpath, 'sample_config.yml')
    
    data = dict(
        log_level='INFO',
        cache_dir='/path/to/cache',
        output_dir='/path/to/output',
        form_types=['10-K', '10-Q'],
        ciks=[129012312, 123219041, 120831241],
        start_year=1995,
        end_year=2019,
        quarters=-1
    )

    with open(full_fpath, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)
    
    return full_fpath

def yaml_config_to_args(args: argparse.Namespace) -> argparse.Namespace:
    """parse yaml config into arguments"""
    if args.config_path:
        config = yaml.safe_load(open(args.config_path, 'r'))
        log_level = config.get('log_level', None)
        cache_dir = config.get('cache_dir', None)
        output_dir = config.get('output_dir', None)
        form_types = config.get('form_types', None)
        ciks = config.get('ciks', None)
        start_year = config.get('start_year', None)
        end_year = config.get('end_year', None)
        quarters = config.get('quarters', None)
        
        if log_level:
            args.log_level = log_level  
        if cache_dir:
            args.cache_dir = cache_dir
        if output_dir:
            args.output_dir = output_dir
        if form_types:
            args.form_types = form_types
        if ciks:
            args.ciks = ciks
        if start_year:
            args.start_year = start_year
        if end_year:
            args.end_year = end_year
        if quarters:
            args.quarters = quarters
            
    return args

def scan_output_dir(output_dir: Path) -> List[str]:
    seen_files = []
    for root, dirs, files in os.walk(output_dir, topdown=False):
        for name in files:
            if name.endswith('.txt') or name.endswith('.html'):
                seen_files.append(name)
    return seen_files

def _check_cache_dir(cache_dir: str) -> str:
    if cache_dir:
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    return cache_dir

def _read_cik_config(cik_path: str) -> List[int]:
    with open(cik_path, 'r') as infile:
        lines = infile.readlines()
        ciks = [ValidateFields.validate_cik(cik.replace('\n', '')) for cik in lines]
    return ciks

def _remove_bad_bytes(lines: List[bytes]) -> List[str]:
    cleanlines = []
    for l in lines:
        try:
            l = l.decode('utf-8')
            l = ftfy.fix_text(l).replace('\n', '').strip()
            cleanlines.append(l)
        except UnicodeDecodeError:
            continue
    return cleanlines


def _to_quarter(month: int) -> str:
    if month > 0 and month <= 3:
        quarter = 'Q1'
    elif month > 3 and month <= 6:
        quarter = 'Q2'
    elif month > 6 and month <= 9:
        quarter = 'Q3'
    else:
        quarter = 'Q4'
    return quarter


class ValidateFields(object):

    @staticmethod
    def validate_date_filed(date_filed: str) -> datetime:
        date_filed = date_filed.strip()
        try:
            date_filed = datetime.strptime(date_filed, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f'VALIDATION ERROR: date_filed: {date_filed} is not datetime (%Y-%m-%d)')
        return date_filed

    @staticmethod
    def validate_cik(cik: str) -> int:
        if isinstance(cik, str):
            cik = cik.strip()
            try:
                cik = int(cik)
            except ValueError:
                raise ValueError(f'VALIDATION ERROR: cik: {cik} is not integers')
        assert isinstance(cik, int)
        return cik

    @staticmethod
    def validate_form_type(form_type: str) -> str:
        form_type = form_type.strip()
        typecheck = form_type.replace(' ', '').replace('-', '').replace('/', '')
        if not typecheck.isupper() and not typecheck.isdigit():
            raise ValueError(f'VALIDATION ERROR: form_type: {form_type} is not upper or digits')
    
        return form_type

    @staticmethod
    def validate_form_name(form_name: str) -> str:
        form_name = form_name.strip()
        if not form_name.endswith('txt'):
            raise ValueError(f'VALIDATION ERROR: form_name: {form_name} does not end with txt')
        return form_name

    @staticmethod
    def validate_company_name(company_name: str) -> str:
        company_name = company_name.strip().upper()
        return company_name

    @staticmethod
    def validate_index_line(cik: str, company_name: str, form_type: str, 
                            date_filed: str, partial_url: str) -> Union[str, str, datetime, str]:
        cik = ValidateFields.validate_cik(cik)
        company_name = ValidateFields.validate_company_name(company_name)
        form_type = ValidateFields.validate_form_type(form_type)
        date_filed = ValidateFields.validate_date_filed(date_filed)
        partial_url = ValidateFields.validate_form_name(partial_url)
        return (cik, company_name, form_type, date_filed, partial_url)