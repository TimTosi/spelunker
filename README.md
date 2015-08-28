Spelunker                         {#mainpage}
=========

Purposes
--------

Spelunker is a software written in Python whose main purpose is to help to build
other Bitcoin oriented tools.
Spelunker offers several capabilities from parsing to user tracking.

Requirements
------------

In order to assure a correct execution, here is a list of the program requirements:
- Database PostgreSQL version 9.4.4
- Python module psycopg2 version 2.6
- Python version 2.7
- Django version 1.7.6
- Little endian system


Installation
------------

In order to parse the blockchain, spelunker needs the .dat files that a bitcoin client
software will download. After having downloaded blockchain file and installed all requirements,
you have to create a new database. You do not need to create any table as the program will do it
for you.

The last setup part is the configuration of the config.ini file. In this file, you have to
provide several information such as the database name, the database username, the password
related to the database user. You also have to set up the path to the directory containing
all bitcoin block files previously downloaded. You will find this file in the spelunker/src
directory. If no password is required for the database access, leave it blank.

Change your current directory for spelunker/src and can now lauch the blockchain parsing by
typing the following command:
    ./main.py


Website Interface
-----------------

If you want to run the website in order to explore the blockchain in a more comfortable way,
change your current directory for spelunker/website/spelunkerWeb and enter the following command:
    ./manage.py runserver 0.0.0.0:8080

You will now be able to access the website from localhost.

Features
--------

1. Blockchain parsing from .dat file
2. Main chain construction
3. Database creation for blockchain exploration
4. Ledger creation for easier currency operations computing

Todo
----

Here is a list of future improvements:
1. Reduce the execution time of the program on
2. Refactor the code in a more pythonic style
3. Support all endianess systems
4. Include support for other database managers
5. Include support for other Bitcoin based cryptocurrencies
