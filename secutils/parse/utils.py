import sys
import json
import ftfy

from bs4 import BeautifulSoup
from IPython.core.display import display, HTML


def percent_bad_parse(num_total, num_bad):
    try:
        percent_bad_parse = num_bad*1.0/num_total
        total_successes = num_total - num_bad
        sys.stdout.write('\rTotal Success: {} -- Percent Bad Parse: {:.2%}'.format(total_successes, percent_bad_parse))
        sys.stdout.flush()
    except ZeroDivisionError:
        pass


def build_html_index_url(header_parts):
    url_builder = 'https://www.sec.gov/Archives/edgar/data/{cik_short}/{accession_short}/{accession_long}-index.htm'
    cik = header_parts['CENTRAL INDEX KEY'].lstrip('0')
    accession_num = header_parts['ACCESSION NUMBER']
    accession_num_trim = accession_num.replace('-', '')
    url = url_builder.format(cik_short=cik, accession_short=accession_num_trim, 
                            accession_long=accession_num)
    return url


def build_index_doc_url(index_url):
    """
    using the index url, capture the table containing all document materials and
    identify the first url pointing to the full document url. 
    
    Args:
        index_url: str - url to documents index site (url containing document addendums, images, and full url)
    
    Return:
        str - url to main page
    """
    base_url = 'https://www.sec.gov'
    content = requests.get(index_url).text
    soup = BeautifulSoup(content, features='html.parser')
    # get tableFile table
    table = soup.find('table', {'class': 'tableFile'})
    # get href to main site url
    main_document_url = table.find('a', href=True).get('href')
    assert main_document_url.endswith('.htm')
    return base_url + main_document_url
    
    
def get_html_document_url(header_parts):
    index_url = build_html_index_url(header_parts)
    main_document_url = build_index_doc_url(index_url)
    return main_document_url


def display_html(txt):
    return display(HTML(txt))


def open_document(fpath: str) -> str:
    with open(fpath, 'r') as infile:
        out = infile.read()
    return out


def write_json_document(fpath: str, json_body: dict) -> None:
    assert fpath.endswith('json'), "Json dumps must end with json"
    with open(fpath, 'w') as outfile:
        json.dump(json_body, outfile)

def read_json_document(fpath: str) -> dict:
    with open(fpath, 'w') as infile:
        input_content = infile.read()
        data = json.loads(input_content)

def clean_text_body(body: str) -> str:
    """
    process body of text removing erroneous characters and 
    spacing. Fix encoding issues. 

    Args:
        body: input str of text to preprocess

    Return:
        str
    """
    body = ''.join([char for char in body if ord(char) <= 128])
    while '  ' in body:
        body = body.replace('  ', ' ')
    body = ftfy.fix_text(body)
    return body.strip()