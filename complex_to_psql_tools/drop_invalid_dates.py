from __future__ import print_function
from __future__ import unicode_literals

import csv
# we have some very big multi-line fields going above the default 128 KB limit
# fortunately they are all still smaller than 1 MB
csv.field_size_limit(max(1024 ** 2, csv.field_size_limit()))

import sys
import iso8601
import time


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
        try:
            parsed = iso8601.parse_date(datestr)
            return parsed.strftime('%Y-%m-%d')
        except iso8601.ParseError:
            pass

    return None


def drop_invalid_dates(fields, csv_reader, csv_writer):
    header = csv_reader.next()
    date_field_indices = {header.index(field) for field in fields}

    csv_writer.writerow(header)
    for row in csv_reader:
        row = list(row)
        for i in date_field_indices:
            # FIXME: it should use the correct date validator
            # in the second release - we need the bad version
            # available for reproducability's sake
            row[i] = date_or_None_9940110(row[i])
        csv_writer.writerow(row)


def main():
    fields, input_csv, output_csv = sys.argv[1:]
    with open(input_csv, 'rb') as input_csv_file:
        with open(output_csv, 'wb') as output_csv_file:
            drop_invalid_dates(
                fields.split(','),
                csv.reader(input_csv_file),
                csv.writer(output_csv_file)
            )

if __name__ == '__main__':
    main()
