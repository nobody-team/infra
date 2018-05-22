import argparse
import os
import re
import sys

EXPORT_TYPE = [
    "TYPE",
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
    "MVIEW",
    "DBLINK",
    "SYNONYM",
    "DIRECTORY"
]

AUTORUN = 0
NAMESPACE = "."
NO_CONSTRAINTS = 0
IMPORT_INDEXES_AFTER = 0
DEBUG = 0
SCHEMA_ONLY = 0
DATA_ONLY = 0
CONSTRAINTS_ONLY = 0
NO_DBCHECK = 0


def die(msg):
    """
    message functions
    :param msg: message to record when exit
    :return:
    """
    print("ERROR: {}".format(msg))
    sys.exit(1)


def call(cmd):
    """
    call system batch
    :param cmd: command to be execute
    :return: exit_status
    """
    print('Execute Command: {}'.format(cmd))
    return os.system(cmd)


def usage():
    print("usage: `basename {0}` [options]\n".format(sys.argv[0]))
    print("\n")
    print("Script used to load exported sql files into PostgreSQL in practical manner\n")
    print("allowing you to chain and automatically import schema and data.\n")
    print("\n")
    print("options:\n")
    print("    -a             import data only\n")
    print("    -b filename    SQL script to execute just after table creation to fix database schema\n")
    print("    -d dbname      database name for import\n")
    print("    -D             enable debug mode, will only show what will be done\n")
    print("    -e encoding    database encoding to use at creation (default: UTF8)\n")
    print("    -f             force no check of user and database existing and do not try to create them\n")
    print("    -h hostname    hostname of the PostgreSQL server (default: unix socket)\n")
    print("    -i             only load indexes, constraints and triggers\n")
    print("    -I             do not try to load indexes, constraints and triggers\n")
    print("    -j cores       number of connection to use to import data or indexes into PostgreSQL\n")
    print("    -l filename    log file where stdout+stderr are redirected (default: stdout)\n")
    print("    -n schema      comma separated list of schema to create\n")
    print("    -o username    owner of the database to create\n")
    print("    -p port        listening port of the PostgreSQL server (default: 5432)\n")
    print("    -P cores       number of tables to process at same time for data import\n")
    print("    -s             import schema only, do not try to import data\n")
    print("    -t export      comma separated list of export type to import (same as ora2pg)\n")
    print("    -U username    username to connect to PostgreSQL (default: peer username)\n")
    print("    -x             import indexes and constraints after data\n")
    print("    -y             reply Yes to all questions for automatic import\n")
    print("\n")
    print("    -?             print help\n")
    print("\n")
    sys.exit(sys.argv[1])


def confirm(msg):
    """
    confirmation before execute
    :return: result of confirm
    """
    if AUTORUN != 0:
        return True
    else:
        if not msg:
            msg = "Are you sure?"
        response = input(msg + " [y/N/q] ")
        if re.search('[yY][eE][sS]|[yY]', response):
            return True
        elif re.search('[qQ][uU][iI][tT]|[qQ]', response):
            sys.exit()
        else:
            return False


def exec_by_psql(import_file, single_transaction=False, user_postgres=False):
    """
    use psql to import file
    :param import_file: relative path of the imported file under namespace
    :param single_transaction: whether add --single-transaction or not
    :param user_postgres: execute with user postgres
    :return: exit_status
    """
    user = 'postgres' if user_postgres else args.db_owner

    if single_transaction:
        return call(
            "psql --single-transaction -h {0} -p {1} -U {2} -d {3} -f {4}/{5}".format(
                args.db_host, args.db_port, user, args.db_name, NAMESPACE, import_file))

    else:
        return call(
            "psql -h {0} -p {1} -U {2} -d {3} -f {4}/{5}".format(
                args.db_host, args.db_port, user, args.db_name, NAMESPACE, import_file))


def exec_by_ora2pg(import_file):
    """
    use ora2pg to import file
    :param import_file: relative path of the imported file under namespace
    :return: exit_status
    """
    return call(
        "ora2pg -j {0} -c config/ora2pg.conf -t LOAD -i {1}/{2}".format(
            args.import_jobs, NAMESPACE, import_file))


def perform_import(import_file, error_msg):
    """
    import the give file
    :param import_file: relative path of the imported file under namespace
    :param error_msg: message shown when exit unsuccessfully
    :return:
    """
    if os.path.exists("{0}/{1}".format(NAMESPACE, import_file)):
        if not args.import_jobs:
            exit_status = exec_by_psql(import_file)
            if exit_status != 0:
                die(error_msg)
        else:
            exit_status = exec_by_ora2pg(import_file)
            if exit_status != 0:
                die(error_msg)


def exec_sql(sql, is_query=True):
    """
    execute in Postgre
    :param sql: sql to execute
    :param is_query: whether is query or execution
    :return: execute result
    """
    if is_query:
        return call(
            "psql -h {0} -p {1} -U {2} -d {3} -Atc '{4}'".format(
                args.db_host, args.db_port, args.db_user, args.db_name, sql)
        )
    else:
        return call(
            "psql -h {0} -p {1} -U {2} -d {3} -c '{4}'".format(
                args.db_host, args.db_port, args.db_user, args.db_name, sql)
        )


def import_constraints():
    """
    Function used to import constraints and indexes
    will import without confirmation
    :return:
    """
    # indexes
    perform_import("schema/tables/INDEXES_table.sql", "can not import indexes.")

    # constraints
    perform_import("schema/tables/CONSTRAINTS_table.sql", "can not import constraints.")

    # foreign keys
    perform_import("schema/schema/tables/FKEYS_table.sql", "can not import foreign keys.")

    # triggers
    import_file = "{0}/schema/triggers/trigger.sql".format(NAMESPACE)
    if args.no_constraints and os.path.exists(import_file):
        exit_status = call(
            "psql --single-transaction -h {0} -p {1} -U {2} -d {3} -f {4}".format(
                args.db_host, args.db_port, args.db_owner, args.db_name, import_file))
        if exit_status != 0:
            die("an error occurs when importing file {}".format(import_file))


def parse_args():
    """
    pass the parameters
    :return: the arg object
    """
    parser = argparse.ArgumentParser(
        description='Script used to load exported sql files into PostgreSQL in practical manner')
    parser.add_argument('-d', action='store', dest='db_name')
    parser.add_argument('-h', action='store', dest='db_host')
    parser.add_argument('-j', action='store', dest='import_jobs')
    parser.add_argument('-p', action='store', dest='db_port')
    parser.add_argument('-o', action='store', dest='db_owner')
    parser.add_argument('-U', action='store', dest='db_user')
    parser.add_argument('-b', action='store', dest='sql_post_script')
    parser.add_argument('-e', action='store', dest='db_encoding')
    parser.add_argument('-n', action='store', dest='db_schema')
    parser.add_argument('-P', action='store', dest='parallel_tables')
    parser.add_argument('-D', action='store_true', dest='debug', default=False)
    parser.add_argument('-I', action='store_true', dest='no_constraints', default=False)
    parser.add_argument('-i', action='store_true', dest='constraints_only', default=False)
    parser.add_argument('-f', action='store_true', dest='no_dbcheck', default=False)
    parser.add_argument('-a', action='store_true', dest='data_only', default=False)
    parser.add_argument('-x', action='store_true', dest='import_indexes_after', default=False)
    parser.add_argument('-s', action='store_true', dest='schema_only', default=False)

    return parser.parse_args()


if __name__ == "__main__":
    # Command line options
    args = parse_args()

    # Check if post tables import SQL script is readable
    if args.sql_post_script:
        if not os.path.exists(args.sql_post_script):
            die("the SQL script {} is not readable.".format(args.sql_post_script))

    # A database name is mandatory
    if not args.db_name:
        die("you must give a PostgreSQL database name (see -d option).")

    # A database owner is mandatory
    if not args.db_owner:
        die("you must give a username to be used as owner of database (see -o option).")

    # Check if the project directory is readable
    if not os.path.exists("{}/schema/tables/table.sql".format(NAMESPACE)):
        die("project directory '{}' is not valid or is not readable.".format(NAMESPACE))

    # If constraints and indexes files are present propose to import these object
    if args.constraints_only == 1:
        import_constraints()
        sys.exit(0)

    # When a PostgreSQL schema list is provided, create them
    if args.data_only == 0:
        if args.no_dbcheck == 0:
            # Create owner user
            user_exists = exec_sql(
                "select usename from pg_user where usename='{}';".format(args.db_owner))
            if not user_exists:
                exit_status = call(
                    "createuser -h {0} -p {1} -U {2} --no-superuser --no-createrole --no-createdb {3}".format(
                        args.db_host, args.db_port, args.db_user, args.db_owner
                    ))
                if exit_status != 0:
                    die("can not create user {}.".format(args.db_owner))
            else:
                print("Database owner {} already exists, skipping creation.".format(args.db_owner))

            # Create database if required
            if not args.db_encoding:
                args.db_encoding = 'UTF8'
            db_exists = exec_sql(
                "select datname from pg_database where datname='{}';".format(args.db_name))
            if not db_exists:
                exit_status = call(
                    "createdb -h {} -p {} -U {} -E {} --owner {} {}".format(
                        args.db_host, args.db_port, args.db_user,
                        args.db_encoding, args.db_owner, args.db_name
                    ))
                if exit_status != 0:
                    die("can not create database {}.".format(args.db_name))
            else:
                exit_status = call(
                    "dropdb -h {} -p {} -U {} {}".format(
                        args.db_host, args.db_port, args.db_user, args.db_name
                    ))
                if exit_status != 0:
                    die("can not drop database {}.".format(args.db_name))
                exit_status = call(
                    "createdb -h {} -p {} -U {} -E {} --owner {} {}".format(
                        args.db_host, args.db_port, args.db_user,
                        args.db_encoding, args.db_owner, args.db_name
                    ))
                if exit_status != 0:
                    die("can not create database {}.".format(args.db_name))

        # When schema list is provided, create them
        if args.db_schema:
            nspace_list = []
            for enspace in args.db_schema.split(','):
                lnspace = enspace.trim().lower()
                exit_status = exec_sql("CREATE SCHEMA {};".format(lnspace), is_query=False)
                if exit_status != 0:
                    die("can not create schema {}.".format(lnspace))
                nspace_list.append(lnspace)
            if nspace_list:
                exit_status = exec_sql("ALTER ROLE {} SET search_path TO {},public;".format(
                    args.db_owner,
                    ','.join(nspace_list)), is_query=False)
                if exit_status != 0:
                    die("can not change search_path.")

        # Then import all files from project directory
        for etype in EXPORT_TYPE:
            if args.no_constraints and etype == "TRIGGER":
                continue
            if etype == "GRANT" or etype == "TABLESPACE":
                continue
            ltype = etype.lower()
            ltype = re.sub(r'y$', 'ie', ltype)
            exit_status = exec_by_psql("schema/{0}s/{0}.sql".format(ltype), single_transaction=True)
            if exit_status != 0:
                die("an error occurs when importing file {0}/schema/{1}s/{1}.sql.".format(NAMESPACE, ltype))
            if args.sql_post_script and etype == "TABLE":
                exit_status = exec_by_psql(args.sql_post_script, single_transaction=True)
                if exit_status != 0:
                    die("an error occurs when importing file {}.".format(args.sql_post_script))

        # If constraints and indexes files are present propose to import these object
        # TODO
        if not args.no_constraints and not args.import_indexes_after:
            args.import_indexes_after = 1

        # Import objects that need superuser priviledge: GRANT and TABLESPACE
        exit_status = exec_by_psql("schema/grants/grant.sql", user_postgres=True)
        if exit_status != 0:
            die("an error occurs when importing file {}/schema/grants/grant.sql.".format(NAMESPACE))
        exit_status = exec_by_psql("schema/tablespaces/tablespace.sql", user_postgres=True)
        if exit_status != 0:
            die("an error occurs when importing file {}/schema/tablespaces/tablespace.sql.".format(NAMESPACE))

    # Check if we must just import schema or proceed to data import too
    if not args.schema_only:
        pgdsn_defined = None
        with open('config/ora2pg.conf') as f:
            line = f.readline();
            if re.search('^PG_DSN', line):
                pgdsn_defined = line.sub('.*dbi:Pg', 'dbi:Pg')
        if not pgdsn_defined:
            if args.db_host:
                pgdsn_defined = "dbi:Pg:dbname={0};host={1}".format(args.db_name, args.db_host)
            else:
                pgdsn_defined = "dbi:Pg:dbname={};".format(args.db_name)
            if args.db_port:
                pgdsn_defined = pgdsn_defined + ";port={}".format(args.db_port)
            else:
                pgdsn_defined = pgdsn_defined + ";port=5432"
        # remove command line option from the DSN string
        pgdsn_defined = pgdsn_defined.sub(' -. ', '')
        # If data file is present propose to import data
        if os.path.exists("{0}/{1}".format(NAMESPACE, 'data/data.sql')):
            exit_status = exec_by_psql('data/data.sql')
            if exit_status != 0:
                die("an error occurs when importing file {}/data/data.sql.".format(NAMESPACE))
        else:
            exit_status = call(
                "ora2pg -j {} -P {} -c config/ora2pg.conf -t COPY --pg_dsn \"{}\" --pg_user {}".format(
                    args.import_jobs, args.parallel_tables, pgdsn_defined, args.db_owner))
            if exit_status != 0:
                die("an error occurs when importing data.")

        if not args.no_constraints and not args.data_only:
            if args.import_indexes_after:
                import_constraints()
