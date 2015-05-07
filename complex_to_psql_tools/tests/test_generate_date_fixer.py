from __future__ import print_function
from __future__ import unicode_literals

import unittest
import pkg_resources
import os
from temp_dir import within_temp_dir
from .util import make_rovat_0_csv, make_rovat_1_csv, make_rovat_2_csv

from complex_to_psql_tools import generate_date_fixer as m


class Test(unittest.TestCase):

    def setUp(self):
        self.r_export_txt_xls = pkg_resources.resource_filename(
            'complex_to_psql_tools',
            'tests/data/R_export.txt.xls'
        )

    def tearDown(self):
        pkg_resources.cleanup_resources()

    @within_temp_dir
    def test_multiple_csvs(self):
        assert os.path.exists(self.r_export_txt_xls)
        make_rovat_0_csv({})
        make_rovat_1_csv({})
        make_rovat_2_csv({})

        commands = sorted(
            m.generate_date_fixer(
                self.r_export_txt_xls,
                input_dir='.',
                output_dir='output'
            )
        )

        expected = [
            'drop-invalid-dates hattol,hatig < rovat_1.csv > output/rovat_1.csv',
            'drop-invalid-dates hattol,hatig < rovat_2.csv > output/rovat_2.csv',
        ]
        self.assertEquals(expected, commands)

    @within_temp_dir
    def test_one_csv(self):
        assert os.path.exists(self.r_export_txt_xls)
        make_rovat_2_csv({})

        commands = sorted(
            m.generate_date_fixer(
                self.r_export_txt_xls,
                input_dir='.',
                output_dir='output'
            )
        )

        expected = [
            'drop-invalid-dates hattol,hatig < rovat_2.csv > output/rovat_2.csv',
        ]
        self.assertEquals(expected, commands)
