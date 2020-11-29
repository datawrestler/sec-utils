from typing import List

from dataclasses import dataclass, field


@dataclass
class FormIDX:
    year: int=field(
        default='',
        metadata={
            'desc': 'Year of file',
        }
    )

    quarter: int=field(
        default='',
        metadata={
            'desc': 'Quarter of file'
        }
    )

    download_url: str=field(
        default='',
        metadata={
            'desc': 'Direct download URL'
        }
    )

    seen_files: List[str]=field(
        default='',
        metadata={
            'desc': 'List of seen files from prior runs',
        }
    )

    cache_dir: str=field(
        default='',
        metadata={
            'desc': 'Cache directory'
        }
    )

    ciks: List[int]=field(
        default='',
        metdata={
            'desc':  'List of CIK numbers'
        }
    )

    form_name: str=

    form_types: List[str]=field(
        default='',
        metadata={
            'desc': 'List of form types to capture'
        }
    )

    master_index: str=field(
        default='',
        metadata={
            'desc': 'Master index'
        }
    )