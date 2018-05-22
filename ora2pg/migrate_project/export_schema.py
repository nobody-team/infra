import os
import re

EXPORT_TYPE = [
    "TABLE",
    "PACKAGE",
    "VIEW",
    "GRANT",
    "SEQUENCE",
    "TRIGGER",
    "FUNCTION",
    "PROCEDURE",
    "TABLESPACE",
    "PARTITION",
    "TYPE",
    "MVIEW",
    "DBLINK",
    "SYNONYM",
    "DIRECTORY"
]

SOURCE_TYPE = [
    "PACKAGE",
    "VIEW",
    "TRIGGER",
    "FUNCTION",
    "PROCEDURE",
    "PARTITION",
    "TYPE",
    "MVIEW"
]

namespace = '.'


def call(cmd):
    """
    call system batch
    :param cmd: command to be execute
    :return: None
    """
    print('Execute Command: {}'.format(cmd))
    os.system(cmd)


def remove_empty_file(file_path):
    """
    remove the file if exist and empty
    :param file_path: path of file to be removed
    :return: None
    """
    if os.path.exists(file_path):
        is_empty = False
        with open(file_path) as f:
            line = f.readline()
            if re.search('Nothing found', line):
                is_empty = True
        if is_empty:
            print("Nothing found {}. Will Remove.".format(file_path))
            os.remove(file_path)


if __name__ == "__main__":
    call(
        "ora2pg -t SHOW_TABLE -c {0}/config/ora2pg.conf > {0}/reports/tables.txt".format(namespace))
    call(
        "ora2pg -t SHOW_COLUMN -c {0}/config/ora2pg.conf > {0}/reports/columns.txt".format(
            namespace))
    call(
        "ora2pg -t SHOW_REPORT -c {0}/config/ora2pg.conf --dump_as_html --estimate_cost > {0}/reports/report.html".format(
            namespace))

    for etype in EXPORT_TYPE:
        ltype = etype.lower()
        ltype = re.sub(r'y$', 'ie', ltype)
        call(
            "ora2pg -p -t {2} -o {1}.sql -b {0}/schema/{1}s -c {0}/config/ora2pg.conf".format(
                namespace, ltype, etype))
        remove_empty_file("{0}/schema/{1}s/{1}.sql".format(namespace, ltype))

    for etype in SOURCE_TYPE:
        ltype = etype.lower()
        ltype = re.sub(r'y$', 'ie', ltype)
        call(
            "ora2pg -t {2} -o {1}.sql -b {0}/sources/{1}s -c {0}/config/ora2pg.conf".format(
                namespace, ltype, etype))
        remove_empty_file("{0}/schema/{1}s/{1}.sql".format(namespace, ltype))

    # To extract data use the following command:
    call("ora2pg -t COPY -o data.sql -b {0}/data -c {0}/config/ora2pg.conf".format(namespace))
