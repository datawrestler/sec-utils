import re
import requests
from collections import namedtuple

from bs4 import BeautifulSoup


class TableOfContents(object):
    
    def __init__(self, sections_of_interest=None):
        if sections_of_interest is None:
            self.sections_of_interest = ['summary', 'risk factor']

    def _clean_toc_text(self, txt):
        txt = txt.replace(' ', '')
        return txt

    def _capture_toc_sections(self, toc):
        """
        capture the start of a section within the table of contents as well as the subsequent section. 

        Args:
            toc: table of toc
            sections_of_interest: list of sections to capture

        Return:
            list of section tuples (name, section_tag_start, section_tag_end)
        """
        all_tuples = []
        sectiontuple = namedtuple('section', 'section_name section_start_tag section_end_tag')
        between_terms = '(\n|\s|\t|.)?'
        
        for section in self.sections_of_interest:
            try:
                re_section = re.compile(section.replace(' ', between_terms), re.IGNORECASE)

                section_index = []

                for ii, t in enumerate(toc):
                    tag_text = t.getText()
                    tag_text = self._clean_toc_text(tag_text)
                    if re_section.search(tag_text):
                        section_index.append(ii)

                section_start = section_index[0]
                section_end = section_start+1

                section_start_tag = toc[section_start].get('href').replace('#', '')
                section_end_tag = toc[section_end].get('href').replace('#', '')
                if section_start_tag == section_end_tag:
                    # sometimes the tags are doubles up - need to slide past the double reference
                    section_end_tag = toc[section_end+1].get('href').replace('#', '')

                cur_tuple = sectiontuple(section_name=section.upper(), section_start_tag=section_start_tag, section_end_tag=section_end_tag)
                all_tuples.append(cur_tuple)
            except IndexError:
                continue

        return all_tuples
    
    def _find_start_end_section_tags(self, soup, section_tuple):
        start_tag = soup.find('a', {'name': section_tuple.section_start_tag})
        end_tag = soup.find('a', {'name': section_tuple.section_end_tag})
        return (section_tuple.section_name, start_tag, end_tag)
    
    def _capture_section(self, start_tag, end_tag):
        section = ''
        for tag in start_tag.nextGenerator():
            if tag == end_tag:
                break
            if hasattr(tag, 'getText'):
                text = tag.getText()
                section += ' ' + text
        return section

    def _clean_section(self, section):
        section = ''.join([char if ord(char) <= 128 else ' ' for char in section])
        section = section.replace('\n', ' ')
        while '  ' in section:
            section = section.replace('  ', ' ')
        section = section.strip()
        return section
    
    def _find_table_of_contents(self, soup):
        keep = None
        out = None
        # capture all tables in document
        tables = soup.findAll('table')
        prospectus_re = re.compile('summary', re.IGNORECASE)
        risk_re = re.compile('risk', re.IGNORECASE)

        # iterate over all tables and look for prospectus and risk factors
        for table in tables:
            prospectus = table.find(['a', 'font'], text=prospectus_re)
            risk = table.find(['a', 'font'], text=risk_re)
            if prospectus and risk:
                keep = table
                # capture elements of table
                toc_a = table.findAll('a', {'href': re.compile('^#')})
                out = toc_a
                break   
        return out
    
    def extract_document_sections(self, header_parts, document_url):
        document_content = requests.get(document_url).text
        soup = BeautifulSoup(document_content, features='html.parser')
        toc = self._find_table_of_contents(soup)
        if toc:
            all_tuples = self._capture_toc_sections(toc)

            for tup in all_tuples:
                try:
                    name, start, end = self._find_start_end_section_tags(soup, tup)
                    section = self._capture_section(start, end)
                    section = self._clean_section(section)
                    header_parts[name] = section
                except AttributeError:
                    continue
        return header_parts