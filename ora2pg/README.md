# Migrate Oracle to PostgreSQL
This document explains how to migrate data from Oracle to PostgreSQL.

## How to Execute
* Eenerate project folder by `ora2pg --init_project migrate_project`
* Override the generated folder with contents within [migrate_project](migrate_project) 
* Update the configure file at [migrate_project/config/ora2pg.conf](migrate_project/config/ora2pg.conf)
* Export schema by executing: [migrate_project/export_schema.py](migrate_project/export_schema.py)
* Import all exported data by executing: [migrate_project/import_all.py](migrate_project/import_all.py)

> For more usage, please refer to [ora2pg documentation](https://ora2pg.darold.net/documentation.html).

## Environment

|Key|Value|
|:-:|:---:|
|OS|Windows 7 64-bit|
|Oracle|12.1.0.2.0 - 64bit|
|PostgreSQL|10.4-1-x64|
|Python|3|


## Background
According to [this page](https://wiki.postgresql.org/wiki/Oracle_to_Postgres_Conversion#External_Tools), there are some exsiting tools and services that are avialable for oracle migration.

In the below, we will introduce how to use the free tool, [ora2pg](http://ora2pg.darold.net/), to export Oracle database to PostgreSQL. It is able to extract the database structure as well as the data.

## Requisitions
Apart from the Oracle and PostgreSQL to migrate data, following tools are also needed:

1. ora2pg-18.2, [Download](https://github.com/darold/ora2pg/releases)
1. ActivePerl-5.22.4.2205, [Download](https://www.activestate.com/activeperl/downloads)
1. Oracle client-12.1.0.2.0, [Download](http://www.oracle.com/technetwork/database/enterprise-edition/downloads/database12c-win64-download-2297732.html)

> * for the ones that used in this instruction, you can find [here](resources).
> * for the latest version, you can download from the provided link beside each tool.

## Installation
1. Install Oracle client
	We need at least a client installad locally to connect to the Oracle database.
	In the following instrunctions, the oracle client is installed at `D:\oracle`
1. Ensure environment variable(change based on your system)
	```
	# Oracle
	LD_LIBRARY_PATH=D:\oracle\client\product\12.1.0\client_1\lib
	ORACLE_HOME=D:\oracle\client\product\12.1.0\client_1
	# PostgreSQL
	POSTGRES_HOME=C:\Program Files\PostgreSQL\10
	POSTGRES_INCLUDE=C:\Program Files\PostgreSQL\10\include
	POSTGRES_LIB=C:\Program Files\PostgreSQL\10\lib
	```
1. Install ActivePerl
	* confirm installation with:
	```
	perl -version
	```
1. Install Perl module: DBI (skipped if using ActivePerl)
1. Install Perl module: DBD-Oracle (skipped if using ActivePerl)
1. Install Perl module: DBD-Pg (skipped if using ActivePerl)
	* execute to install
	```
	perl -MCPAN -e "install Bundle::DBD::Pg"
	```
1. Install ora2pg
	* unzip the downlowned package and switch to the extracted folder
	* execute to install
	```
	perl Makefile.PL
	dmake && dmake install
	```
	* verify installation
	```
	ora2pg --version
	```

## Configuration
After the installation of ora2pg, a new folder will be created at `C:\ora2pg`.(could be changed in `ora2pg\Makefile.PL`).
The configuration file for ora2pg is `ora2pg_dist.conf`. 
The explaination for those settings could be found in the README file or [here](https://github.com/darold/ora2pg).

Please update following configurations based on your system:

|config|value|remark|
|:-----|:----|:-----|
|ORACLE_HOME|D:\oracle\client\product\12.1.0\client_1|-|
|ORACLE_DSN|dbi:Oracle:host=localhost;sid=test;port=1521|change the connection accoardingly|
|ORACLE_USER|system|change to the super admin, Note that if you can it is better to login as Oracle super admin to avoid grants problem during the database scan and be sure that nothing is missing.|
|ORACLE_PWD|manager|change the password accoardingly|
|PG_DSN|dbi:Pg:dbname=postgres;host=localhost;port=5432 |change the connection accoardingly|
|PG_USER|test|change the login user accoardingly|
|PG_PWD|test|change the password accoardingly|
|REPLACE_COLS|apms_propertybehavior(notnull:not_null)|change the column name that is ineligible in Postgre. Refer to [Postgre Keywords](https://www.postgresql.org/docs/10/static/sql-keywords-appendix.html)|
|SCHEMA|-|add space-seprated schemas to export, otherwise export all|
|TYPE|TABLE PACKAGE COPY VIEW GRANT SEQUENCE TRIGGER FUNCTION PROCEDURE TABLESPACE TYPE PARTITION|-|
|USE_TABLESPACE|1|export table space as well|
|FORCE_OWNER|1|use the same user as in Oracle if necessary|
|OUTPUT_DIR|D:\Conversion\migration|-|
|TRANSACTION|readonly|-|
|DATADIFF_WORK_MEM|1024 MB|-|
|DATADIFF_TEMP_BUFFERS|2048 MB|-|
|ALLOW|-|restrict the objects to be exported by its name|
|DEBUG|1|Trace all to stderr, otherwise will terminate silently|
|DROP_FKEY|1|Refer the doc for DEFER_FKEY/DROP_FKEY|
|TRUNCATE_TABLE|1|Add a TRUNCATE TABLE instruction before loading data on COPY and INSERT export|
|FILE_PER_FKEYS|1|Export foreign key declaration to be saved in a separate file. convenient for importing through file|

## Initialize 


## Migration
* use intermediate file to migrate(if `PG_DSN` is not set)
	- export data and table DDL
		```
		ora2pg -d -c C:\ora2pg\ora2pg_dist.conf -b D:\Conversion\migration -t COPY -o data.sql
		```
		this will generate 3 files in `D:\Conversion\migration`:
		* output.sql: table DDL
		* data.sql: data of each tables
		* FKEYS_output.sql: foreign keys(if FILE_PER_FKEYS is set to 1)
	- import into Postgre(pay attention to the path separator in Windows)
		```
		\i D:/Conversion\migration/output.sql
		\i D:/Conversion\migration/data.sql
		\i D:/Conversion\migration/FKEYS_output.sql
		```

* migrate from Oracle to PostgreSQL directly(if `PG_DSN` is set)
	```
	ora2pg -d -c C:\ora2pg\ora2pg_dist.conf -l D:\Conversion\migration\ora2pg.log
	```

#### Why ActiveState Perl

As mentioned in the [README](https://github.com/darold/ora2pg) of ora2pg:
>  It seems that compiling DBD::Oracle from CPAN on Windows can be a
    struggle and there be little documentation on that (mostly outdated and
    not working). Installing the free version of ActiveState Perl
    (http://www.activestate.com/activeperl) could help as they seems to have
    an already packaged DBD::Oracle easy to install.
    
#### About the .gitkeep under `migrate_project`
Those extra `.gitkeep` files are added to maintain the folder structure and generated by below script:
```python
import os

for root, dirs, files in os.walk('.'):
    for d in dirs:
        print(os.path.join(root, d))
        open(os.path.join(root, d, '.gitkeep'), 'w')
```

## Trouble Shooting



