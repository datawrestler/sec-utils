import os
import unittest
from datetime import datetime

from secutils.utils import (scan_output_dir, _remove_bad_bytes, 
                            _to_quarter, ValidateFields, 
                            _read_cik_config, generate_config)

class TestUtils(unittest.TestCase):

    def test_quarter(self):
        month = 12
        quarter = _to_quarter(month)
        msg = f"Quarter should be Q4 - got {quarter} instead"
        self.assertEqual(quarter, 'Q4', msg)

    def test_generate_config(self):
        path = 'data'
        generate_config(path)
        self.assertTrue(os.path.exists(os.path.join(path, 'sample_config.yml')), msg='Sample config not being created from generate_config')

    def test_cik_config(self):
        dirname = os.path.dirname(__file__)
        cik_config_path = os.path.join(dirname, 'data/test_cik_config.txt')
        ciks = _read_cik_config(cik_config_path)
        check = all([isinstance(x, int) for x in ciks])
        failed_type_check = set([type(x) for x in ciks])
        msg = f"_read_cik_config not casting CIK's to ints w/types: {failed_type_check}"
        self.assertTrue(check, msg)

    def test_validate_date(self):
        dte = '2016-6-2'
        dte = ValidateFields.validate_date_filed(dte)
        msg = f"incorrect return type. Expected datetime.datetime but got {type(dte)}"
        self.assertIsInstance(dte, datetime, msg)

    def test_validate_cik(self):
        cik = '10001291'
        cik = ValidateFields.validate_cik(cik)
        msg = f"Incorrect return type. Expected int but got {type(cik)}"
        self.assertIsInstance(cik, int, msg)

    def test_validate_form_name(self):
        form_name = '098308310432342.html'
        with self.assertRaises(ValueError):
            ValidateFields.validate_form_name(form_name)

    def test_validate_company_name(self):
        co_name = ' peloton inc. '
        new_co_name = ValidateFields.validate_company_name(co_name)
        msg = f"Expected upper case and stripped company name. Got: {co_name}"
        self.assertEqual(new_co_name, co_name.upper().strip(), msg)

    def test_validate_form_type(self):
        form_type = '10k'
        with self.assertRaises(ValueError):
            ValidateFields.validate_form_type(form_type)

    def test_validate_index_line(self):
        cik = '903210934'
        company_name = 'MAGIC COMPANY'
        form_type = '10-K'
        date_filed = '2019-7-2'
        partial_url = '/edgar/data/12038324102011234.txt'
        results = ValidateFields.validate_index_line(cik, company_name, form_type, date_filed, partial_url)
        msg = f"Unexpected length of return object - expected 5 got {len(results)} w/objects: {results}"
        self.assertEqual(len(results), 5, msg)

    def test_scan_output_dir(self):
        dirname = os.path.dirname(__file__)
        scan_dir = os.path.join(dirname, 'data')
        seen_files = scan_output_dir(scan_dir)
        text_files = list(filter(lambda x: x.endswith('txt'), os.listdir(scan_dir)))
        msg = f"Expected files to be found - got {len(seen_files)} when expected {len(text_files)}"
        self.assertSequenceEqual(seen_files, text_files, msg)
    

if __name__ == "__main__":
    unittest.main()

    