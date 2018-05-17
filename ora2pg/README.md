# Migrate Oracle to PostgreSQL
This document explains how to migrate data from Oracle to PostgreSQL.

## Environment
|-|-|
|:-:|:---:|
|OS|Windows 7 64-bit|
|Oracle|12.1.0.2.0 - 64bit|
|PostgreSQL|10.4-1-x64|


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
1. Update environment variable(change based on your system)
	```
	LD_LIBRARY_PATH=D:\oracle\client\product\12.1.0\client_1\lib
	ORACLE_HOME=D:\oracle\client\product\12.1.0\client_1
	```
1. Install ActivePerl
	* confirm installation with:
	```
	perl -version
	```
1. Install Perl module:  DBI (skipped if using ActivePerl)
1. Install Perl module:  DBD-Oracle (skipped if using ActivePerl)
1. Install DBD-Pg
	* execute to install
	```
	perl -MCPAN -e 'install Bundle::DBD::Pg'
	```
1. Install ora2pg
	* unzip the downlowned package and switch to the extracted folder
	* execute to install
	```
	perl Makefile.PL
	dmake && dmake install
	```

## Configuration
After the installation of ora2pg, a new folder will be created at `C:\ora2pg`.(could be changed `ora2pg\Makefile.PL`).
The configuration file for ora2pg is `ora2pg_dist.conf`. 
The explaination for those settings could be found in the README file or [here](https://github.com/darold/ora2pg).

Please update following configurations based on your system:
|config|value|remark|
|:----:|:---:|:----:|
|ORACLE_HOME|D:\oracle\client\product\12.1.0\client_1|-|




#### Why ActiveState Perl

As mentioned in the [README](https://github.com/darold/ora2pg) of ora2pg:
>  It seems that compiling DBD::Oracle from CPAN on Windows can be a
    struggle and there be little documentation on that (mostly outdated and
    not working). Installing the free version of ActiveState Perl
    (http://www.activestate.com/activeperl) could help as they seems to have
    an already packaged DBD::Oracle easy to install.



