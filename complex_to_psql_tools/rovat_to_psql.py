from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os.path
import sys

# shell combinator magic:
from plumbum import local
csv_to_psql = local['csv_to_psql']


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--fields-meta')
    parser.add_argument('csv_file')
    return parser.parse_args(argv)


def import_command(argv):
    args = parse_args(argv)

    csv_file = args.csv_file
    fields_meta = args.fields_meta

    basename, ext = os.path.splitext(csv_file)
    assert ext.lower() == '.csv'

    tablename = os.path.basename(basename)

    command = csv_to_psql[
        '--create-table', tablename,
        '--primary-key', 'ceg_id,alrovat_id'
    ]

    if fields_meta and os.path.isfile(fields_meta):
        command = command['--fields={}'.format(fields_meta)]

    return (command < csv_file) > sys.stdout


def main():
    command = import_command(sys.argv[1:])
    # print(command)
    command()


if __name__ == '__main__':
    main()
