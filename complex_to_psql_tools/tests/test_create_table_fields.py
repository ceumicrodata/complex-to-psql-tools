from __future__ import print_function
from __future__ import unicode_literals

import unittest
from temp_dir import within_temp_dir
from complex_to_psql_tools import create_table_fields as m
import pkg_resources
from glob import glob


class Test_create_table_fields(unittest.TestCase):

    def setUp(self):
        self.r_export_txt_xls = pkg_resources.resource_filename(
            'complex_to_psql_tools',
            'tests/data/R_export.txt.xls'
        )

    def tearDown(self):
        pkg_resources.cleanup_resources()

    @within_temp_dir
    def test_number_of_files_created(self):
        m.create_table_fields(self.r_export_txt_xls)

        files = glob('rovat_?.fields')
        self.assertEquals(3, len(files))
