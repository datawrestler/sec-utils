import json
import ftfy


def open_document(fpath: str) -> str:
    with open(fpath, 'r') as infile:
        out = infile.read()
    return out

def write_json_document(fpath: str, json_body: dict) -> None:
    assert fpath.endswith('json'), "Json dumps must end with json"
    with open(fpath, 'w') as outfile:
        json.dump(json_body, outfile)


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