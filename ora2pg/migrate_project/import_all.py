# ---------------------------------------------------------
#
# Python translation of the original import_all.sh
#
# ---------------------------------------------------------

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime

NAMESPACE = "."

start_time = time.perf_counter()
print("export_schema starts at: {}".format(str(datetime.now())))


def call(cmd, confirm_msg, error_msg, callback=None):
    """
    call system batch
    :param cmd: command to be execute
    :param confirm_msg: confirm message prompt before execution
    :param error_msg: error message shown when unsuccessfully
    :param callback: execution callback
    :return: None
    """
    if (not confirm_msg) or confirm(confirm_msg):
        print("Running: {}".format(cmd))
        if not args.debug:
            status = os.system(cmd)
            if status != 0:
                die(error_msg)
        if callback:
            callback()


def exec_by_psql(import_file,
                 confirm_msg=None,
                 error_msg=None,
                 single_transaction=False,
                 user_postgres=False):
    """
    use psql to import file
    :param import_file: relative path of the imported file under namespace
    :param confirm_msg: messge prompt before execution
    :param error_msg: error message when unsuccessfully
    :param single_transaction: whether add --single-transaction or not
    :param user_postgres: execute with user postgres
    :return: None
    """
    user = 'postgres' if user_postgres else args.db_owner

    if single_transaction:
        call(
            "psql --single-transaction -h {0} -p {1} -U {2} -d {3} -f {4}/{5}".format(
                args.db_host, args.db_port, user, args.db_name, NAMESPACE, import_file),
            confirm_msg,
            error_msg)

    else:
        call(
            "psql -h {0} -p {1} -U {2} -d {3} -f {4}/{5}".format(
                args.db_host, args.db_port, user, args.db_name, NAMESPACE, import_file),
            confirm_msg,
            error_msg)


def exec_by_ora2pg(import_file,
                   confirm_msg=None,
                   error_msg=None):
    """
    use ora2pg to import file
    :param import_file: relative path of the imported file under namespace
    :param confirm_msg: confirm message prompt
    :param error_msg: error message shown when fails
    :return: None
    """
    call(
        "ora2pg -j {0} -c config/ora2pg.conf -t LOAD -i {1}/{2}".format(
            args.import_jobs, NAMESPACE, import_file),
        confirm_msg,
        error_msg)


def exec_sql(sql, is_query=True):
    """
    execute in Postgre
    :param sql: sql to execute
    :param is_query: whether is query or execution
    :return: execute result for query or exit code for execution
    """
    if is_query:
        result = subprocess.run(["psql -h {0} -p {1} -U {2} -d {3} -Atc \"{4}\"".format(
            args.db_host, args.db_port, args.db_user, args.db_name, sql)], stdout=subprocess.PIPE)
        return result.stdout
    else:
        result = subprocess.run(["psql -h {0} -p {1} -U {2} -d {3} -c \"{4}\"".format(
            args.db_host, args.db_port, args.db_user, args.db_name, sql)], stdout=subprocess.PIPE)
        return result.returncode


def die(msg):
    """
    show error message and exit with error
    :param msg: message to record when exit
    :return:
    """
    print("ERROR: {}".format(msg))
    print("export_schema ends successfully in {}s at {}?".format(
        (time.perf_counter() - start_time) / 60, str(datetime.now())))
    sys.exit(1)


def confirm(msg):
    """
    confirmation before execute
    :return: True for agree to proceed, False for reject, or quit directly
    """
    if args.autorun:
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


def perform_import_file(import_file,
                        confirm_msg,
                        error_msg,
                        import_jobs,
                        single_transaction=False,
                        user_postgres=False):
    """
    import the give file
    :param import_file: relative path of the imported file under namespace
    :param confirm_msg: confirm message prompt before execution
    :param error_msg: message shown when exit unsuccessfully
    :param import_jobs: number of jobs used to import by ora2pg
    :param single_transaction whether to add --single_transaction for psql command
    :param user_postgres: whether to use postgres as the user or use the args.db_owner
    :return:
    """
    if os.path.exists("{0}/{1}".format(NAMESPACE, import_file)):
        if confirm(confirm_msg):
            if not import_jobs:
                exec_by_psql(import_file,
                             error_msg=error_msg,
                             single_transaction=single_transaction,
                             user_postgres=user_postgres)
            else:
                exec_by_ora2pg(import_file, error_msg=error_msg)


def import_constraints(import_jobs):
    """
    Function used to import constraints and indexes
    :param import_jobs: number of jobs used by ora2pg
    :return:
    """
    # indexes
    perform_import_file("schema/tables/INDEXES_table.sql",
                        "Would you like to import indexes from {}/schema/tables/INDEXES_table.sql?".format(
                            NAMESPACE),
                        "can not import indexes.",
                        import_jobs=import_jobs)

    # constraints
    perform_import_file("schema/tables/CONSTRAINTS_table.sql",
                        "Would you like to import constraints from {}/schema/tables/CONSTRAINTS_table.sql?".format(
                            NAMESPACE),
                        "can not import constraints.",
                        import_jobs=import_jobs)

    # foreign keys
    perform_import_file("schema/schema/tables/FKEYS_table.sql",
                        "Would you like to import foreign keys from {}/schema/tables/FKEYS_table.sql?".format(
                            NAMESPACE),
                        "can not import foreign keys.",
                        import_jobs=import_jobs)

    # triggers
    perform_import_file("schema/triggers/trigger.sql",
                        "Would you like to import TRIGGER from {}/schema/triggers/trigger.sql?".format(
                            NAMESPACE),
                        "an error occurs when importing file {}/schema/triggers/trigger.sql.".format(
                            NAMESPACE),
                        import_jobs=import_jobs,
                        single_transaction=True)


def parse_args():
    """
    Command line options
    :return: the arg object
    """
    parser = argparse.ArgumentParser(
        description='Script used to load exported sql files into PostgreSQL in practical manner')
    parser.add_argument('-a', action='store_true', dest='data_only',
                        default=False,
                        help="import data only")
    parser.add_argument('-b', action='store', dest='sql_post_script',
                        help="SQL script to execute just after table creation to fix database schema")
    parser.add_argument('-d', action='store', dest='db_name',
                        help="database name for import")
    parser.add_argument('-D', action='store_true', dest='debug',
                        default=False,
                        help="enable debug mode, will only show what will be done")
    parser.add_argument('-e', action='store', dest='db_encoding',
                        help="database encoding to use at creation (default: UTF8)")
    parser.add_argument('-f', action='store_true', dest='no_dbcheck',
                        default=False,
                        help="force no check of user and database existing and do not try to create them")
    parser.add_argument('-h', action='store', dest='db_host',
                        help="hostname of the PostgreSQL server (default: unix socket)")
    parser.add_argument('-i', action='store_true', dest='constraints_only',
                        default=False,
                        help="only load indexes, constraints and triggers")
    parser.add_argument('-I', action='store_true', dest='no_constraints',
                        default=False,
                        help="do not try to load indexes, constraints and triggers")
    parser.add_argument('-j', action='store', dest='import_jobs',
                        help="number of connection to use to import data or indexes into PostgreSQL")
    parser.add_argument('-n', action='store', dest='db_schema',
                        help="comma separated list of schema to create")
    parser.add_argument('-o', action='store', dest='db_owner',
                        help="owner of the database to create")
    parser.add_argument('-p', action='store', dest='db_port',
                        help="listening port of the PostgreSQL server (default: 5432)")
    parser.add_argument('-P', action='store', dest='parallel_tables',
                        help="number of tables to process at same time for data import")
    parser.add_argument('-s', action='store_true', dest='schema_only',
                        default=False,
                        help="import schema only, do not try to import data")
    parser.add_argument('-t', action='store', dest='export_type',
                        default="TYPE,TABLE,PACKAGE,VIEW,GRANT,SEQUENCE,TRIGGER,FUNCTION,PROCEDURE,TABLESPACE,PARTITION,MVIEW,DBLINK,SYNONYM,DIRECTORY",
                        help="comma separated list of export type to import (same as ora2pg)")
    parser.add_argument('-U', action='store', dest='db_user',
                        help="username to connect to PostgreSQL (default: peer username)")
    parser.add_argument('-x', action='store_true', dest='import_indexes_after',
                        default=False,
                        help="import indexes and constraints after data")
    parser.add_argument('-y', action='store_true', dest='autorun',
                        default=False,
                        help="reply Yes to all questions for automatic import")

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
    if args.constraints_only:
        if confirm("Would you like to load indexes, constraints and triggers?"):
            import_constraints(args.import_jobs)
        sys.exit(0)

    # When a PostgreSQL schema list is provided, create them
    if not args.data_only:
        if not args.no_dbcheck:
            # Create owner user
            user_exists = exec_sql(
                "select usename from pg_user where usename='{}';".format(args.db_owner))
            if not user_exists:
                call(
                    "createuser -h {0} -p {1} -U {2} --no-superuser --no-createrole --no-createdb {3}".format(
                        args.db_host, args.db_port, args.db_user, args.db_owner),
                    "Would you like to create the owner of the database {}?".format(args.db_owner),
                    "can not create user {}.".format(args.db_owner))

            else:
                print("Database owner {} already exists, skipping creation.".format(args.db_owner))

            # Create database if required
            if not args.db_encoding:
                args.db_encoding = 'UTF8'
            db_exists = exec_sql(
                "select datname from pg_database where datname='{}';".format(args.db_name))
            if not db_exists:
                call(
                    "createdb -h {} -p {} -U {} -E {} --owner {} {}".format(
                        args.db_host, args.db_port, args.db_user,
                        args.db_encoding, args.db_owner, args.db_name),
                    "Would you like to create the database {}?".format(args.db_name),
                    "can not create database {}.".format(args.db_name))
            else:
                call(
                    "dropdb -h {} -p {} -U {} {}".format(
                        args.db_host, args.db_port, args.db_user, args.db_name),
                    "Would you like to drop the database {} before recreate it?".format(args.db_name),
                    "can not drop database {}.".format(args.db_name)

                )
                call(
                    "createdb -h {} -p {} -U {} -E {} --owner {} {}".format(
                        args.db_host, args.db_port, args.db_user,
                        args.db_encoding, args.db_owner, args.db_name),
                    confirm_msg=None,
                    error_msg="can not create database {}.".format(args.db_name))

        # When schema list is provided, create them
        if args.db_schema:
            nspace_list = []
            for enspace in args.db_schema.split(','):
                lnspace = enspace.trim().lower()

                call("psql -h {0} -p {1} -U {2} -d {3} -c \"CREATE SCHEMA {4};\"".format(
                    args.db_host, args.db_port, args.db_user, args.db_name, lnspace),
                    "Would you like to create schema {} in database {}?".format(lnspace, args.db_name),
                    "can not create schema {}.".format(lnspace),
                    callback=lambda: nspace_list.append(lnspace))

            if nspace_list:
                call(
                    "psql -h {0} -p {1} -U {2} -d {3} -c \"ALTER ROLE {4} SET search_path TO {5},public;\"".format(
                        args.db_host, args.db_port, args.db_user, args.db_name, args.db_owner,
                        ','.join(nspace_list)),
                    "Would you like to change search_path of the database owner?",
                    "can not change search_path.")

        # Then import all files from project directory
        for etype in args.export_type:
            if args.no_constraints and etype == "TRIGGER":
                continue
            if etype == "GRANT" or etype == "TABLESPACE":
                continue
            ltype = etype.lower()
            ltype = re.sub(r'y$', 'ie', ltype)

            perform_import_file("schema/{0}s/{0}.sql".format(ltype),
                                "Would you like to import $etype from {0}/schema/{1}s/{1}.sql?".format(
                                    NAMESPACE,
                                    ltype),
                                "an error occurs when importing file {0}/schema/{1}s/{1}.sql?".format(
                                    NAMESPACE,
                                    ltype),
                                import_jobs=None,
                                single_transaction=True)

            if args.sql_post_script and etype == "TABLE":
                exec_by_psql(args.sql_post_script,
                             "Would you like to execute SQL script {}?".format(args.sql_post_script),
                             "an error occurs when importing file {}.".format(args.sql_post_script),
                             single_transaction=True)

        # If constraints and indexes files are present propose to import these object
        if not args.no_constraints and not args.import_indexes_after:
            if confirm("Would you like to process indexes and constraints before loading data?"):
                args.import_indexes_after = False
                import_constraints(args.import_jobs)
            else:
                args.import_indexes_after = True

        # Import objects that need superuser priviledge: GRANT and TABLESPACE
        perform_import_file("schema/grants/grant.sql",
                            "Would you like to import GRANT from {}/schema/grants/grant.sql?".format(
                                NAMESPACE),
                            "an error occurs when importing file {}/schema/grants/grant.sql.".format(
                                NAMESPACE),
                            import_jobs=None,
                            user_postgres=True)
        perform_import_file("schema/tablespaces/tablespace.sql",
                            "Would you like to import TABLESPACE from {}/schema/tablespaces/tablespace.sql?".format(
                                NAMESPACE),
                            "an error occurs when importing file {}/schema/tablespaces/tablespace.sql.".format(
                                NAMESPACE),
                            import_jobs=None,
                            user_postgres=True)

    # Check if we must just import schema or proceed to data import too
    if not args.schema_only:
        pgdsn_defined = None
        with open('config/ora2pg.conf') as f:
            for line in f:
                if re.search(r'^PG_DSN', line):
                    pgdsn_defined = re.sub(r'.*dbi:Pg', 'dbi:Pg', line)
                    if not pgdsn_defined:
                        if args.db_host:
                            pgdsn_defined = "dbi:Pg:dbname={0};host={1}".format(args.db_name,
                                                                                args.db_host)
                        else:
                            # default to unix socket
                            pgdsn_defined = "dbi:Pg:dbname={};".format(args.db_name)
                    break

        if args.db_port:
            pgdsn_defined = pgdsn_defined + ";port={}".format(args.db_port)
        else:
            pgdsn_defined = pgdsn_defined + ";port=5432"

        # remove command line option from the DSN string
        pgdsn_defined = pgdsn_defined.sub(' -. ', '')

        # If data file is present propose to import data
        if os.path.exists("{0}/data/data.sql".format(NAMESPACE)):
            exec_by_psql('data/data.sql',
                         "Would you like to import data from {}/data/data.sql?".format(NAMESPACE),
                         "an error occurs when importing file {}/data/data.sql.".format(NAMESPACE))
        else:
            call("ora2pg -j {} -P {} -c config/ora2pg.conf -t COPY --pg_dsn \"{}\" --pg_user {}".format(
                args.import_jobs, args.parallel_tables, pgdsn_defined, args.db_owner),
                "Would you like to import data from Oracle database directly into PostgreSQL?",
                "an error occurs when importing data.")

        if not args.no_constraints and not args.data_only:
            if args.import_indexes_after:
                import_constraints(args.import_jobs)

    print("export_schema ends successfully in {}s at {}?".format(
        (time.perf_counter() - start_time) / 60, str(datetime.now())))
