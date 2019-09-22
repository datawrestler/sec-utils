import os
import random
import unittest

import pandas as pd

from bulkedgar.edgar import (FileUtils, File, 
                       FormIDX, build_dir_structure, 
                       download_docs, SECContainer)


class TestEdgar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.form = FormIDX(year=2017, quarter=2, cache_dir='data')
        dirname = os.path.dirname(__file__)
        cls.tmpdir = os.path.join(dirname, 'data', 'tmp')
        os.makedirs(cls.tmpdir, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        for f in os.listdir(cls.tmpdir):
            os.remove(os.path.join(cls.tmpdir, f))
        os.rmdir(cls.tmpdir)

    def test_form_from_cache(self):
        msg = f"Incorrect cache type - expected pd.DataFrame, got {type(self.form.master_index)}"
        self.assertIsInstance(self.form.master_index, pd.DataFrame, msg)

    def test_get_master_zip_index(self):
        form = FormIDX(year=2017, quarter=3)
        master_index = form._get_master_zip_index()
        msg = f"Incorrect cache type - expected pd.DataFrame, got {type(master_index)}"
        self.assertIsInstance(master_index, pd.DataFrame, msg)

    def test_parse_index_lines(self):
        lines = [
            '90810312|MAGIC COMPANY|10-K|2017-2-9|/edgar/data/08912031231.txt',
            '32472152|MAGICAL COMPANY|10-K|2015-2-9|/edgar/data/32472152.txt',
            '24275120|SUPER MAGIC COMPANY|10-K|2017-1-30|/edgar/data/24275120.txt',
            '20347120|AWESOME SUPER MAGIC COMPANY|10-K|2012-2-9|/edgar/data/20347120.txt',
        ]

        master_index = self.form._parse_index_lines(lines)
        msg = f"Incorrect cache type - expected pd.DataFrame, got {type(master_index)}"
        self.assertIsInstance(master_index, pd.DataFrame, msg)

    def test_filter_form_type(self):
        self.form.form_types = ['10-K']
        master_index = self.form._filter_form_type(self.form.master_index)
        msg = f"Expected 1 form type - got {master_index['Form Type'].unique()}"
        self.assertEqual(master_index['Form Type'].nunique(), 1, msg)

    def test_filter_seen_files(self):
        original_shape = self.form.master_index.shape[0]
        seen_files = self.form.master_index.iloc[0:1000]['fname'].tolist()
        self.form.seen_files = seen_files
        master_index = self.form._filter_seen_files(self.form.master_index)
        check = original_shape - 1000
        msg = f"Expected shape: {check} - received shape: {master_index.shape[0]}"
        self.assertLess(master_index.shape[0], original_shape, msg)

    def test_index_to_files(self):
        files = self.form.index_to_files()
        check = all([isinstance(f, File) for f in files])
        not_file_type = [type(f) for f in files if not isinstance(f, File)]
        msg = f"Expected all types to be File - got {set(not_file_type)}"
        self.assertTrue(check, msg)

    def test_file_download(self):
        files = self.form.index_to_files()
        f = random.choice(files)
        f.download_file(self.tmpdir)
        check = os.path.exists(f.download_file_dir)
        msg = f"Unable to download ({f.download_file_dir}): {f.company_name} - {f.date_filed} - {f.file_download_url} - {f.cik_number}"
        self.assertTrue(check, msg)

    def test_sec_container(self):
        container1 = SECContainer()
        container1.to_download = set()
        container1.to_download.add('file1.txt')
        container1.to_download.add('file2.txt')
        container1.to_download.add('file3.txt')
        container2 = SECContainer()
        msg = f"Multiple SECContainers not equal: container1: {container1.to_download} - container2: {container2.to_download}"
        self.assertSetEqual(container1.to_download, container2.to_download, msg)

if __name__ == '__main__':
    unittest.main()