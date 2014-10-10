from __future__ import print_function
from __future__ import unicode_literals

import csv
# we have some very big multi-line fields going above the default 128 KB limit
# fortunately they are all still smaller than 1 MB
csv.field_size_limit(max(1024 ** 2, csv.field_size_limit()))

import sys
import iso8601
import time
import argparse


def date_or_None_9940110(datestr):
    # this version is WRONG, but something like this was used to
    # this allows 9940110 to pass through, which would fail to load
    # into postgresql from csv, yet it was surprisingly imported
    # as 9940-01-10 (rovat_3)
    #    ceg_id   | alrovat_id |   hattol   | hatig |          nev           |
    # ------------+------------+------------+-------+------------------------+
    #  0106313015 |          1 | 9940-01-10 |       | THE PHOENIX "J" "M" BT |
    # In [1]: import time
    # In [2]: time.strptime('9940110', '%Y%m%d')
    # Out[2]: time.struct_time(tm_year=9940, tm_mon=1, tm_mday=10, tm_hour=...
    # In [3]: time.strftime('%Y-%m-%d', time.strptime('9940110', '%Y%m%d'))
    # Out[3]: '9940-01-10'

    if datestr:
        try:
            parsed = time.strptime(datestr, '%Y%m%d')
            return time.strftime('%Y-%m-%d', parsed)
        except ValueError:
            pass

    return None


def date_or_None(datestr):
    if datestr:
        parsed = None
        try:
            parsed = iso8601.parse_date(datestr)
            try:
                return parsed.strftime('%Y-%m-%d')
            except ValueError:
                pass
        except iso8601.ParseError:
            pass

    return None


def drop_invalid_dates(fields, csv_reader, csv_writer, invalid_dropper):
    header = csv_reader.next()
    date_field_indices = {header.index(field) for field in fields}

    csv_writer.writerow(header)
    for row in csv_reader:
        row = list(row)
        for i in date_field_indices:
            # FIXME: it should use the correct date validator
            # in the second release - we need the bad version
            # available for reproducability's sake
            row[i] = invalid_dropper(row[i])
        csv_writer.writerow(row)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='''\
        substitutes None for bad dates on input,
        and also converts formats dates as YYYY-MM-DD
        '''
    )
    parser.add_argument(
        '--bad-parser',
        dest='invalid_dropper',
        default=date_or_None,
        action='store_const',
        const=date_or_None_9940110,
        help='''
        This option is exclusively for reproducing the original
        Complex2012 import!

        (When used an old, bad date parser is used instead of the iso8601
        parser, that will e.g. convert date 9940110 to 9940-01-10,
        while can not interpret 1994-01-10 as it contains dashes.)
        ''',
    )

    def comma_separated_fields_to_list(fields):
        return fields.split(',')
    parser.add_argument(
        'fields',
        type=comma_separated_fields_to_list,
        help='''
        comma separated fields that should be checked.
        e.g. hattol,hatig,bkelt,tkelt
        ''',
    )

    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    drop_invalid_dates(
        args.fields,
        csv.reader(sys.stdin),
        csv.writer(sys.stdout),
        args.invalid_dropper,
    )

if __name__ == '__main__':
    main()
