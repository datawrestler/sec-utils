import re
import numpy as np
from datetime import datetime

import ftfy
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import namedtuple

from secutils.parse.utils import (clean_text_body, open_document, 
                                  write_json_document)


class HeaderParser(object):

    def __init__(self, output_dir: str):
        self.bad_parses = []
        self.output_dir = output_dir

    def _remove_jpg_image_data(self, body):
        """
        remove image data embedded at bottom of SEC filings

        Args:
            body: str - input text
        
        Return:
            str - body with jpg image data removed
        """
        init_start = len(body)+1
        p = re.compile("GRAPHIC")
        for m in p.finditer(body):
            if m.start() < init_start:
                init_start = m.start()
        
        return body[:init_start] 

    def _get_acceptance_datetime(self, header):
        for pt in header:
            if 'ACCEPTANCE-DATETIME' in pt:
                dte = pt.split('>')[-1]
                return dte   

    def _tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def _text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self._tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def _prepare_header_and_body(self, txt):
        start_header = re.compile('<SEC-HEADER>')
        end_header = re.compile('</SEC-HEADER>')
        start_idx = start_header.search(txt).span()[-1]
        end_idx = end_header.search(txt).span()[0]

        header = txt[start_idx:end_idx]
        parts = [pt for pt in header.split('\n') if pt != '']
        body = txt[end_idx:]
        
        return parts, body

    def _clean_parts(self, part):
        parts = [part for part in part.split('\t') if part != '']
        if len(parts) == 2:
            header = parts[0].replace(':', '')
            value = parts[-1]
        else:
            header, value = None, None
        return header, value

    def _parse_header_into_parts(self, parts):
        
        clean_header_parts = {}
        seen_zip_count = 0
        addr_prefix = ['BUSINESS', 'MAILING']
        for pt in parts:
            header, val = self._clean_parts(pt)
            if header in ['STREET 1', 'STREET 2', 'CITY', 'STATE', 'ZIP']:
                
                header = f"{addr_prefix[seen_zip_count]} {header}"
                if 'ZIP' in header:
                    seen_zip_count = 1
            if header is not None:
                clean_header_parts[header] = val
                
        acceptance_date = self._get_acceptance_datetime(parts)
        clean_header_parts['ACCEPTANCE DATE'] = acceptance_date
        return clean_header_parts

    def parse(self, fpath):
        text = open_document(fpath)
        parts, body = self._prepare_header_and_body(text)
        clean_header_parts = self._parse_header_into_parts(parts)
        try:
            text_body = self._remove_jpg_image_data(self._text_from_html(body))
            text_body = clean_text_body(text_body)
            clean_header_parts['BODY'] = text_body
        except (UnboundLocalError, TypeError):
            text_body = None 
            self.bad_parses.append(fpath)

        clean_header_parts['BODY'] = text_body
        clean_header_parts['PATH'] = fpath
        return clean_header_parts



