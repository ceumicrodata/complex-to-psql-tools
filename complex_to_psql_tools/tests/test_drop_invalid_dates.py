from __future__ import print_function
from __future__ import unicode_literals

import unittest
from io import BytesIO
import csv
from complex_to_psql_tools import drop_invalid_dates as m


class Test_date_or_None(unittest.TestCase):

    def test_invalid_date_is_replaced_w_None(self):
        self.assertIsNone(m.date_or_None('2014-13-41'))

    def test_malformed_date_is_replaced_w_None(self):
        self.assertIsNone(m.date_or_None('2003/12/12'))

    def test_malformed_date2_is_replaced_w_None(self):
        self.assertIsNone(m.date_or_None('13-13-13'))

    def test_iso_basic_dates_are_kept(self):
        self.assertEquals('20140429', m.date_or_None('20140429'))

    def test_iso_extended_dates_are_kept(self):
        self.assertEquals('2014-04-29', m.date_or_None('2014-04-29'))

    def test_malformed_9940110(self):
        self.assertIsNone(m.date_or_None('9940110'))


class Test_drop_invalid_dates(unittest.TestCase):

    def test(self):
        input = [
            'a,date1,b,date2,c',
            'a,date1,b,date2,c',
            'a,20140429,b,20131231,c',
        ]

        output = BytesIO()

        m.drop_invalid_dates(
            ['date2', 'date1'],
            csv.reader(input),
            csv.writer(output)
        )

        self.assertEquals(
            [
                'a,date1,b,date2,c',
                'a,,b,,c',
                'a,20140429,b,20131231,c',
            ],
            unicode(output.getvalue()).splitlines()
        )
