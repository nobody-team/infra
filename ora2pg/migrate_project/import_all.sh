#!/bin/sh
#-------------------------------------------------------------------------------
#
# Script used to load exported sql files into PostgreSQL in practical manner
# allowing you to chain and automatically import schema and data.
#
# Generated by Ora2Pg, the Oracle database Schema converter, version 18.2
#
#-------------------------------------------------------------------------------

EXPORT_TYPE="TYPE TABLE PACKAGE VIEW GRANT SEQUENCE TRIGGER FUNCTION PROCEDURE TABLESPACE PARTITION MVIEW DBLINK SYNONYM DIRECTORY"
AUTORUN=0
NAMESPACE=.
NO_CONSTRAINTS=0
IMPORT_INDEXES_AFTER=0
DEBUG=0
SCHEMA_ONLY=0
DATA_ONLY=0
CONSTRAINTS_ONLY=0
NO_DBCHECK=0


# Message functions
die() {
    echo "ERROR: $1" 1>&2
    exit 1
}

usage() {
    echo "usage: `basename $0` [options]"
    echo ""
    echo "Script used to load exported sql files into PostgreSQL in practical manner"
    echo "allowing you to chain and automatically import schema and data."
    echo ""
    echo "options:"
    echo "    -a             import data only"
    echo "    -b filename    SQL script to execute just after table creation to fix database schema"
    echo "    -d dbname      database name for import"
    echo "    -D             enable debug mode, will only show what will be done"
    echo "    -e encoding    database encoding to use at creation (default: UTF8)"
    echo "    -f             force no check of user and database existing and do not try to create them"
    echo "    -h hostname    hostname of the PostgreSQL server (default: unix socket)"
    echo "    -i             only load indexes, constraints and triggers"
    echo "    -I             do not try to load indexes, constraints and triggers"
    echo "    -j cores       number of connection to use to import data or indexes into PostgreSQL"
    echo "    -l filename    log file where stdout+stderr are redirected (default: stdout)"
    echo "    -n schema      comma separated list of schema to create"
    echo "    -o username    owner of the database to create"
    echo "    -p port        listening port of the PostgreSQL server (default: 5432)"
    echo "    -P cores       number of tables to process at same time for data import"
    echo "    -s             import schema only, do not try to import data"
    echo "    -t export      comma separated list of export type to import (same as ora2pg)"
    echo "    -U username    username to connect to PostgreSQL (default: peer username)"
    echo "    -x             import indexes and constraints after data"
    echo "    -y             reply Yes to all questions for automatic import"
    echo
    echo "    -?             print help"
    echo
    exit $1
}

# Function to emulate Perl prompt function
confirm () {

    msg=$1
    if [ "$AUTORUN" != "0" ]; then
	true
    else
	    if [ -z "$msg" ]; then
		msg="Are you sure? [y/N/q]"
	    fi
	    # call with a prompt string or use a default
	    read -r -p "${msg} [y/N/q] " response
	    case $response in
		[yY][eE][sS]|[yY]) 
		    true
		    ;;
		[qQ][uU][iI][tT]|[qQ]) 
		    exit
		    ;;
		*)
		    false
		    ;;
	    esac
    fi
}

# Function used to import constraints and indexes
import_constraints () {
	if [ -r "$NAMESPACE/schema/tables/INDEXES_table.sql" ]; then
		if confirm "Would you like to import indexes from $NAMESPACE/schema/tables/INDEXES_table.sql?" ; then
			if [ -z "$IMPORT_JOBS" ]; then
				echo "Running: psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/tables/INDEXES_table.sql"
				if [ $DEBUG -eq 0 ]; then
					psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/tables/INDEXES_table.sql
					if [ $? -ne 0 ]; then
						die "can not import indexes."
					fi
				fi
			else
				echo "Running: ora2pg -c config/ora2pg.conf -t LOAD -i $NAMESPACE/schema/tables/INDEXES_table.sql"
				if [ $DEBUG -eq 0 ]; then
					ora2pg$IMPORT_JOBS -c config/ora2pg.conf -t LOAD -i $NAMESPACE/schema/tables/INDEXES_table.sql
					if [ $? -ne 0 ]; then
						die "can not import indexes."
					fi
				fi
			fi
		fi
	fi

	if [ -r "$NAMESPACE/schema/tables/CONSTRAINTS_table.sql" ]; then
		if confirm "Would you like to import constraints from $NAMESPACE/schema/tables/CONSTRAINTS_table.sql?" ; then
			if [ -z "$IMPORT_JOBS" ]; then
				echo "Running: psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/tables/CONSTRAINTS_table.sql"
				if [ $DEBUG -eq 0 ]; then
					psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/tables/CONSTRAINTS_table.sql
					if [ $? -ne 0 ]; then
						die "can not import constraints."
					fi
				fi
			else
				echo "Running: ora2pg$IMPORT_JOBS -c config/ora2pg.conf -t LOAD -i $NAMESPACE/schema/tables/CONSTRAINTS_table.sql"
				if [ $DEBUG -eq 0 ]; then
					ora2pg$IMPORT_JOBS -c config/ora2pg.conf -t LOAD -i $NAMESPACE/schema/tables/CONSTRAINTS_table.sql
					if [ $? -ne 0 ]; then
						die "can not import constraints."
					fi
				fi
			fi
		fi
	fi

	if [ -r "$NAMESPACE/schema/tables/FKEYS_table.sql" ]; then
		if confirm "Would you like to import foreign keys from $NAMESPACE/schema/tables/FKEYS_table.sql?" ; then
			if [ -z "$IMPORT_JOBS" ]; then
				echo "Running: psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/tables/FKEYS_table.sql"
				if [ $DEBUG -eq 0 ]; then
					psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/tables/FKEYS_table.sql
					if [ $? -ne 0 ]; then
						die "can not import foreign keys."
					fi
				fi
			else
				echo "Running: ora2pg$IMPORT_JOBS -c config/ora2pg.conf -t LOAD -i $NAMESPACE/schema/tables/FKEYS_table.sql"
				if [ $DEBUG -eq 0 ]; then
					ora2pg$IMPORT_JOBS -c config/ora2pg.conf -t LOAD -i $NAMESPACE/schema/tables/FKEYS_table.sql
					if [ $? -ne 0 ]; then
						die "can not import foreign keys."
					fi
				fi
			fi
		fi
	fi

	if [ $NO_CONSTRAINTS -eq 1 ] && [ -r "$NAMESPACE/schema/triggers/trigger.sql" ]; then
		if confirm "Would you like to import TRIGGER from $NAMESPACE/schema/triggers/trigger.sql?" ; then
			echo "Running: psql --single-transaction$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/triggers/trigger.sql"
			if [ $DEBUG -eq 0 ]; then
				psql --single-transaction$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/triggers/trigger.sql
				if [ $? -ne 0 ]; then
					die "an error occurs when importing file $NAMESPACE/schema/triggers/trigger.sql."
				fi
			fi
		fi
	fi
}

# Command line options
while getopts "b:d:e:h:j:l:n:o:p:P:t:U:aDfiIsyx?"  opt; do
    case "$opt" in
	a) DATA_ONLY=1;;
	b) SQL_POST_SCRIPT=$OPTARG;;
        d) DB_NAME=$OPTARG;;
        D) DEBUG=1;;
        e) DB_ENCODING=" -E $OPTARG";;
	f) NO_DBCHECK=1;;
        h) DB_HOST=" -h $OPTARG";;
        i) CONSTRAINTS_ONLY=1;;
        I) NO_CONSTRAINTS=1;;
        j) IMPORT_JOBS=" -j $OPTARG";;
        l) LOGFILE=$OPTARG;;
        n) DB_SCHEMA=$OPTARG;;
        o) DB_OWNER=$OPTARG;;
        p) DB_PORT=" -p $OPTARG";;
        P) PARALLEL_TABLES=" -P $OPTARG";;
        s) SCHEMA_ONLY=1;;
        t) EXPORT_TYPE=$OPTARG;;
        U) DB_USER=" -U $OPTARG";;
	x) IMPORT_INDEXES_AFTER=1;;
        y) AUTORUN=1;;
        "?") usage 1;;
        *) die "Unknown error while processing options";;
    esac
done

# Check if post tables import SQL script is readable
if [ ! -z "$SQL_POST_SCRIPT" ]; then
	if [ ! -r "$SQL_POST_SCRIPT" ]; then
		die "the SQL script $SQL_POST_SCRIPT is not readable."
	fi
fi

# A database name is mandatory
if [ -z "$DB_NAME" ]; then
	die "you must give a PostgreSQL database name (see -d option)."
fi

# A database owner is mandatory
if [ -z "$DB_OWNER" ]; then
	die "you must give a username to be used as owner of database (see -o option)."
fi

# Check if the project directory is readable
if [ ! -r "$NAMESPACE/schema/tables/table.sql" ]; then
	die "project directory '$NAMESPACE' is not valid or is not readable."
fi

# If constraints and indexes files are present propose to import these object
if [ $CONSTRAINTS_ONLY -eq 1 ]; then
	if confirm "Would you like to load indexes, constraints and triggers?" ; then
		import_constraints
	fi
	exit 0
fi

# When a PostgreSQL schema list is provided, create them
if [ $DATA_ONLY -eq 0 ]; then
	if [ $NO_DBCHECK  -eq 0 ]; then
		# Create owner user
    user_exists=`psql -d $DB_NAME$DB_HOST$DB_PORT$DB_USER -Atc "select usename from pg_user where usename='$DB_OWNER';"`
		if [ "a$user_exists" = "a" ]; then
			if confirm "Would you like to create the owner of the database $DB_OWNER?" ; then
				echo "Running: createuser$DB_HOST$DB_PORT$DB_USER --no-superuser --no-createrole --no-createdb $DB_OWNER"
				if [ $DEBUG -eq 0 ]; then
					createuser$DB_HOST$DB_PORT$DB_USER --no-superuser --no-createrole --no-createdb $DB_OWNER
					if [ $? -ne 0 ]; then
						die "can not create user $DB_OWNER."
					fi
				fi
			fi
		else
			echo "Database owner $DB_OWNER already exists, skipping creation."
		fi

		# Create database if required
		if [ "a$DB_ENCODING" = "a" ]; then
			DB_ENCODING=" -E UTF8"
		fi
    db_exists=`psql -d $DB_NAME$DB_HOST$DB_PORT$DB_USER -Atc "select datname from pg_database where datname='$DB_NAME';"`
		if [ "a$db_exists" = "a" ]; then
			if confirm "Would you like to create the database $DB_NAME?" ; then
				echo "Running: createdb$DB_HOST$DB_PORT$DB_USER$DB_ENCODING --owner $DB_OWNER $DB_NAME"
				if [ $DEBUG -eq 0 ]; then
					createdb$DB_HOST$DB_PORT$DB_USER$DB_ENCODING --owner $DB_OWNER $DB_NAME
					if [ $? -ne 0 ]; then
						die "can not create database $DB_NAME."
					fi
				fi
			fi
		else
			if confirm "Would you like to drop the database $DB_NAME before recreate it?" ; then
				echo "Running: dropdb$DB_HOST$DB_PORT$DB_USER $DB_NAME"
				if [ $DEBUG -eq 0 ]; then
					dropdb$DB_HOST$DB_PORT$DB_USER $DB_NAME
					if [ $? -ne 0 ]; then
						die "can not drop database $DB_NAME."
					fi
				fi
				echo "Running: createdb$DB_HOST$DB_PORT$DB_USER$DB_ENCODING --owner $DB_OWNER $DB_NAME"
				if [ $DEBUG -eq 0 ]; then
					createdb$DB_HOST$DB_PORT$DB_USER$DB_ENCODING --owner $DB_OWNER $DB_NAME
					if [ $? -ne 0 ]; then
						die "can not create database $DB_NAME."
					fi
				fi
			fi
		fi
	fi

	# When schema list is provided, create them
	if [ "a$DB_SCHEMA" != "a" ]; then
		nspace_list=''
		for enspace in $(echo $DB_SCHEMA | tr "," "\n")
		do
			lnspace=`echo $enspace | tr '[:upper:]' '[:lower:]'`
			if confirm "Would you like to create schema $lnspace in database $DB_NAME?" ; then
				echo "Running: psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -c \"CREATE SCHEMA $lnspace;\""
				if [ $DEBUG -eq 0 ]; then
					psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -c "CREATE SCHEMA $lnspace;"
					if [ $? -ne 0 ]; then
						die "can not create schema $DB_SCHEMA."
					fi
				fi
				nspace_list="$nspace_list$lnspace,"
			fi
		done
		# Change search path of the owner
		if [ "a$nspace_list" != "a" ]; then
			if confirm "Would you like to change search_path of the database owner?" ; then
				echo "Running: psql$DB_HOST$DB_PORT$DB_USER -d $DB_NAME -c \"ALTER ROLE $DB_OWNER SET search_path TO ${nspace_list}public;\""
				if [ $DEBUG -eq 0 ]; then
					psql$DB_HOST$DB_PORT$DB_USER -d $DB_NAME -c "ALTER ROLE $DB_OWNER SET search_path TO ${nspace_list}public;"
					if [ $? -ne 0 ]; then
						die "can not change search_path."
					fi
				fi
			fi
		fi
	fi

	# Then import all files from project directory
	for etype in $(echo $EXPORT_TYPE | tr "," "\n")
	do

		if [ $NO_CONSTRAINTS -eq 1 ] && [ $etype = "TRIGGER" ]; then
			continue
		fi

		if [ $etype = "GRANT" ] || [ $etype = "TABLESPACE" ]; then
			continue
		fi

		ltype=`echo $etype | tr '[:upper:]' '[:lower:]'`
		ltype=`echo $ltype | sed 's/y$/ie/'`
		if [ -r "$NAMESPACE/schema/${ltype}s/$ltype.sql" ]; then
			if confirm "Would you like to import $etype from $NAMESPACE/schema/${ltype}s/$ltype.sql?" ; then
				echo "Running: psql --single-transaction $DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/${ltype}s/$ltype.sql"
				if [ $DEBUG -eq 0 ]; then
					psql --single-transaction $DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/schema/${ltype}s/$ltype.sql
					if [ $? -ne 0 ]; then
						die "an error occurs when importing file $NAMESPACE/schema/${ltype}s/$ltype.sql."
					fi
				fi
			fi
		fi
		if [ ! -z "$SQL_POST_SCRIPT" ] && [ $etype = "TABLE" ]; then
			if confirm "Would you like to execute SQL script $SQL_POST_SCRIPT?" ; then
				echo "Running: psql --single-transaction$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $SQL_POST_SCRIPT"
				if [ $DEBUG -eq 0 ]; then
					psql --single-transaction$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $SQL_POST_SCRIPT
					if [ $? -ne 0 ]; then
						die "an error occurs when importing file $SQL_POST_SCRIPT."
					fi
				fi
			fi
		fi
	done

	# If constraints and indexes files are present propose to import these object
	if [ $NO_CONSTRAINTS -eq 0 ] && [ $IMPORT_INDEXES_AFTER -eq 0 ]; then
		if confirm "Would you like to process indexes and constraints before loading data?" ; then
			IMPORT_INDEXES_AFTER=0
			import_constraints
		else
			IMPORT_INDEXES_AFTER=1
		fi
	fi

	# Import objects that need superuser priviledge: GRANT and TABLESPACE
	if [ -r "$NAMESPACE/schema/grants/grant.sql" ]; then
		if confirm "Would you like to import GRANT from $NAMESPACE/schema/grants/grant.sql?" ; then
			echo "Running: psql $DB_HOST$DB_PORT -U postgres -d $DB_NAME -f $NAMESPACE/schema/grants/grant.sql"
			if [ $DEBUG -eq 0 ]; then
				psql $DB_HOST$DB_PORT -U postgres -d $DB_NAME -f $NAMESPACE/schema/grants/grant.sql
				if [ $? -ne 0 ]; then
					die "an error occurs when importing file $NAMESPACE/schema/grants/grant.sql."
				fi
			fi
		fi
	fi
	if [ -r "$NAMESPACE/schema/tablespaces/tablespace.sql" ]; then
		if confirm "Would you like to import TABLESPACE from $NAMESPACE/schema/tablespaces/tablespace.sql?" ; then
			echo "Running: psql $DB_HOST$DB_PORT -U postgres -d $DB_NAME -f $NAMESPACE/schema/tablespaces/tablespace.sql"
			if [ $DEBUG -eq 0 ]; then
				psql $DB_HOST$DB_PORT -U postgres -d $DB_NAME -f $NAMESPACE/schema/tablespaces/tablespace.sql
				if [ $? -ne 0 ]; then
					die "an error occurs when importing file $NAMESPACE/schema/tablespaces/tablespace.sql."
				fi
			fi
		fi
	fi
fi


# Check if we must just import schema or proceed to data import too
if [ $SCHEMA_ONLY -eq 0 ]; then
	# set the PostgreSQL datasource
	pgdsn_defined=`grep "^PG_DSN" config/ora2pg.conf | sed 's/.*dbi:Pg/dbi:Pg/'`
	if [ "a$pgdsn_defined" = "a" ]; then
		if [ "a$DB_HOST" != "a" ]; then
			pgdsn_defined="dbi:Pg:dbname=$DB_NAME;host=$DB_HOST"
		else
      #default to unix socket
      pgdsn_defined="dbi:Pg:dbname=$DB_NAME;"
    fi
		if [ "a$DB_PORT" != "a" ]; then
			pgdsn_defined="$pgdsn_defined;port=$DB_PORT"
		else
			pgdsn_defined="$pgdsn_defined;port=5432"
		fi
	fi

	# remove command line option from the DSN string
	pgdsn_defined=`echo "$pgdsn_defined" | sed 's/ -. //g'`

	# If data file is present propose to import data
	if [ -r "$NAMESPACE/data/data.sql" ]; then
		if confirm "Would you like to import data from $NAMESPACE/data/data.sql?" ; then
			echo "Running: psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/data/data.sql"
			if [ $DEBUG -eq 0 ]; then
				psql$DB_HOST$DB_PORT -U $DB_OWNER -d $DB_NAME -f $NAMESPACE/data/data.sql
				if [ $? -ne 0 ]; then
					die "an error occurs when importing file $NAMESPACE/data/data.sql."
				fi
			fi
		fi
	else
		# Import data directly from PostgreSQL
		if confirm "Would you like to import data from Oracle database directly into PostgreSQL?" ; then
			echo "Running: ora2pg$IMPORT_JOBS$PARALLEL_TABLES -c config/ora2pg.conf -t COPY --pg_dsn \"$pgdsn_defined\" --pg_user $DB_OWNER"
			if [ $DEBUG -eq 0 ]; then
				ora2pg$IMPORT_JOBS$PARALLEL_TABLES -c config/ora2pg.conf -t COPY --pg_dsn "$pgdsn_defined" --pg_user $DB_OWNER
				if [ $? -ne 0 ]; then
					die "an error occurs when importing data."
				fi
			fi
		fi
	fi

	if [ $NO_CONSTRAINTS -eq 0 ] && [ $DATA_ONLY -eq 0 ]; then
		# Import indexes and constraint after data
		if [ $IMPORT_INDEXES_AFTER -eq 1 ]; then
			import_constraints
		fi
	fi
fi

exit 0

