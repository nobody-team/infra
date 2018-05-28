# Migrate Oracle to PostgreSQL
This document explains how to migrate data from Oracle to PostgreSQL.

## How to Execute
* Generate project folder by `ora2pg --init_project migrate_project`
* Override the generated folder with contents within [migrate_project](migrate_project) 
* Update the configure file at [migrate_project/config/ora2pg.conf](migrate_project/config/ora2pg.conf)
* Change the client authentication in file `POSTGRE_INSTALL/data/pg_hba.conf` to `trust`, like:

|TYPE|DATABASE|USER|ADDRESS|METHOD|
|:--:|:------:|:--:|:-----:|:----:|
|host|all|all|127.0.0.1/32|trust|
    
* Export schema by executing: [migrate_project/export_schema.py](migrate_project/export_schema.py)
* Change user password in [migrate_project/schema/grants/grant.sql](migrate_project/schema/grants/grant.sql)
* Execute the `CREATE USER` statement and remove them from [migrate_project/schema/grants/grant.sql](migrate_project/schema/grants/grant.sql)
* Change the path of tablespace in [migrate_project/schema/tablespaces/tablespace.sql](migrate_project/schema/tablespaces/tablespace.sql)
* Execute the `CREATE TABLESPACE`/`ALTER TABLESPACE` statement and remove them from [migrate_project/schema/tablespaces/tablespace.sql](migrate_project/schema/tablespaces/tablespace.sql)
* Change directories in [migrate_project/schema/directories/directorie.sql](migrate_project/schema/directories/directorie.sql)
* Check Oracle type conversion, like `NVARCHAR2`(`TEXT`), in [migrate_project/schema/packages/package.sql](migrate_project/schema/packages/package.sql)
* Import all exported data by executing: [migrate_project/import_all.py](migrate_project/import_all.py)

> * For more usage, please refer to [ora2pg documentation](https://ora2pg.darold.net/documentation.html).
> * Since there are no packages in PostgreSQL, there are no package-level variables either. Instead of packages, use schemas to organize your functions into groups.
> 

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
#### ORA-01652: unable to extend temp segment by 129 in tablespace TEMP
```
create temporary tablespace TEMP2 tempfile 'C:\COMPANY_SERVERS\CJKDB\SINGAPORE\ORADATA\SINGA\TEMPSINGA2.DBF' size 32G autoextend on;

alter database default temporary tablespace TEMP2;
```

#### ORA-08177 can't serialize access for this transaction
change the transaction setting in `ora2pg_dist.conf`


#### Can't call method "do" on an undefined value at C:/Perl64/site/lib/Ora2Pg.pm line 5221.
according to this [issue](https://github.com/darold/ora2pg/issues/542)
> You can not use data export (COPY) together with other export type. Commit [45fe50d](https://github.com/darold/ora2pg/commit/45fe50d9bfca9d4b56b66432c680f8fe95540cec) add a note about that in the documentation.

#### Oracle Syntax: `IS TABLE OF`
Usually the statement looks like: 
```
TYPE workdays IS TABLE OF DATE
```

In order to translate, we need to find the equivalent type in PostgreSQL, like `timestamp`.
This statement can be translated as: 

```sql
workdays timestamp[];
```
the way to access should also change from `workdays(idx)` to `workdays[idx]` 

#### Oracle Syntax: `IS RECORD`
Usually the statement looks like: 
```sql
TYPE payinfo IS RECORD(
    payment     Date,
    remark      VARCHAR
    );
```
This statement can be translated as: 
```sql
CREATE TYPE payinfo AS (
    paydate   timestamp,
    remark    text
    );
```

#### Oracle Syntax: `CURSOR FOR`
Usually the statement looks like: 
```sql
xyz CURSOR FOR select * from address ad
                        join city ct on ad.city_id = ct.city_id;    
xyz_row xyz;
```
Just need to change:
```sql
xyz_row RECORD;
```
> @see: https://stackoverflow.com/questions/22339628/cursor-based-records-in-postgresql

#### Oracle Syntax: `CURSOR XXX IS`
use
```sql
XXX CURSOR FOR
```

#### Oracle Syntax: `dbms_sql`
> @see: [Executing Dynamic Commands](https://www.postgresql.org/docs/8.3/static/plpgsql-statements.html#PLPGSQL-STATEMENTS-EXECUTING-DYN)

#### ERROR:  syntax error at or near "BEGIN"
The PostgreSQL does not supported nested FUNCTION. 
In this case, need to handle/convert manually.

#### ERROR:  functions cannot have more than 100 arguments
This is a known limitation and it's very difficult to change since the limitation is baked very deeply into the existing catalog structure.
Some options/workarounds available to overcome this is:
* Use arrays rather than individual arguments
* Use record data-types to the functions rather than individual arguments

> @see: [Function Fails with "ERROR: functions cannot have more than 100 arguments"](https://discuss.pivotal.io/hc/en-us/articles/204396563-Function-Fails-with-ERROR-functions-cannot-have-more-than-100-arguments-)

#### ERROR:  column "rowid" does not exist
There is `ctid` column which is equivalent for rowid.

> @see: [5.4. System Columns](https://www.postgresql.org/docs/current/static/ddl-system-columns.html)


## Reference
* [Oracle to PostgreSQL Migration](http://www.sqlines.com/oracle-to-postgresql)
* [Porting from Oracle PL/SQL](https://www.postgresql.org/docs/9.6/static/plpgsql-porting.html)
* [Porting from Oracle to PostgreSQL](https://www.cs.cmu.edu/~pmerson/docs/OracleToPostgres.pdf)