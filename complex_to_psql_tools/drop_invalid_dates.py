from __future__ import print_function
from __future__ import unicode_literals
import csv
# we have some very big multi-line fields going above the default 128 KB limit
# fortunately they are all still smaller than 1 MB
csv.field_size_limit(max(1024 ** 2, csv.field_size_limit()))
import sys
import iso8601


def date_or_None(datestr):
    if datestr:
        try:
            iso8601.parse_date(datestr)
            return datestr
            # parsed = iso8601.parse_date(datestr)
            # return parsed.strftime('%Y-%m-%d')
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
            row[i] = date_or_None(row[i])
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
