This directory contains all of the necessary files to import csv files into a database that was built
according the LOST data model.

Contents:
README.txt - this README file.
import_data.sh - a script which will make a new directory to hold exported and run the python file that will export the data.
import.py - to be run by export_data.sh to generate several csv files which contain LOST data that is ready for importing.
imp_rdy1 - directory which contains the csv files from the database 'hw' from the first round of testing.
dump - directory which contains the csv files from the database 'hw' from the second round of testing.
lost_data - directory which contains the csv files from the LOST database for the final round of testing.

Usage (input_dir is the directory which contains the csv files which are to be imported into the database):

$ createdb <dbname>

$ cd ..

$ ./preflight.sh <dbname>

$ cd import

$ bash import_data.sh <dbname> <input_dir>
