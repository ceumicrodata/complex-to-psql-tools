from __future__ import print_function
from __future__ import unicode_literals

import unittest
from io import BytesIO
import csv
from complex_to_psql_tools import drop_invalid_dates as m


class Test_date_or_None_9940110(unittest.TestCase):

    convert = staticmethod(m.date_or_None_9940110)

    def test_malformed_9940110(self):
        self.assertEquals('9940-01-10', self.convert('9940110'))

    def test_invalid_date_is_replaced_w_None(self):
        self.assertIsNone(self.convert('2014-13-41'))

    def test_malformed_date_is_replaced_w_None(self):
        self.assertIsNone(self.convert('2003/12/12'))

    def test_malformed_date2_is_replaced_w_None(self):
        self.assertIsNone(self.convert('13-13-13'))

    def test_iso_basic_dates_are_kept(self):
        self.assertEquals('2014-04-29', self.convert('20140429'))

    def test_iso_extended_dates_are_kept(self):
        self.assertIsNone(self.convert('2014-04-29'))

    def test_old_date_is_replaced_w_None(self):
        self.assertIsNone(self.convert('11120720'))


class Test_date_or_None(unittest.TestCase):

    convert = staticmethod(m.date_or_None)

    def test_invalid_date_is_replaced_w_None(self):
        self.assertIsNone(self.convert('2014-13-41'))

    def test_malformed_date_is_replaced_w_None(self):
        self.assertIsNone(self.convert('2003/12/12'))

    def test_malformed_date2_is_replaced_w_None(self):
        self.assertIsNone(self.convert('13-13-13'))

    def test_iso_basic_dates_are_OK(self):
        self.assertEquals('2014-04-29', self.convert('20140429'))

    def test_iso_extended_dates_are_OK(self):
        self.assertEquals('2014-04-29', self.convert('2014-04-29'))

    def test_malformed_9940110_is_replaced_w_None(self):
        self.assertIsNone(self.convert('9940110'))

    def test_old_date_is_replaced_w_None(self):
        self.assertIsNone(self.convert('11120720'))


class Test_drop_invalid_dates(unittest.TestCase):

    def drop_invalid_dates(self, invalid_dropper):
        input = [
            'a,date1,b,date2,c',
            'a,date1,b,date2,c',
            'a,20140429,b,2013-12-31,c',
        ]

        output = BytesIO()

        m.drop_invalid_dates(
            ['date2', 'date1'],
            csv.reader(input),
            csv.writer(output),
            invalid_dropper,
        )

        return unicode(output.getvalue())

    def test_legacy_bad(self):
        output = self.drop_invalid_dates(m.date_or_None_9940110)
        self.assertEquals(
            [
                'a,date1,b,date2,c',
                'a,,b,,c',
                'a,2014-04-29,b,,c',
            ],
            output.splitlines()
        )

    def test_iso8601(self):
        output = self.drop_invalid_dates(m.date_or_None)
        self.assertEquals(
            [
                'a,date1,b,date2,c',
                'a,,b,,c',
                'a,2014-04-29,b,2013-12-31,c',
            ],
            output.splitlines()
        )
