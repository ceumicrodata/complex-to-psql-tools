from __future__ import print_function
from __future__ import unicode_literals

import sys
import complex_schema
from ConfigParser import ConfigParser

FIELD_CEGID = 'field:ceg_id'
FIELD_ALROVAT_ID = 'field:alrovat_id'
TYPE = 'type'
NULLABLE = 'nullable'
FALSE = 'false'


def create_table_fields(r_export_txt_xls):
    tables = complex_schema.read_tables(r_export_txt_xls)

    for table in tables:
        cfg = ConfigParser(defaults={TYPE: 'varchar'})

        cfg.add_section(FIELD_CEGID)
        cfg.set(FIELD_CEGID, NULLABLE, FALSE)
        cfg.add_section(FIELD_ALROVAT_ID)
        cfg.set(FIELD_ALROVAT_ID, NULLABLE, FALSE)
        cfg.set(FIELD_ALROVAT_ID, TYPE, 'integer')

        for field in table.fields:
            if field.type == 'date':
                section = 'field:{}'.format(field.name)
                cfg.add_section(section)
                cfg.set(section, TYPE, 'date')

        with open('{}.fields'.format(table.name), 'w') as file:
            cfg.write(file)


def main():
    r_export_txt_xls, = sys.argv[1:]
    create_table_fields(r_export_txt_xls)


if __name__ == '__main__':
    main()
