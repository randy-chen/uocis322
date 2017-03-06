This directory contains all of the necessary files to export data from a database that was built
according the LOST data model.

Contents:
README.txt - this README file.
export_data.sh - a script which will make a new directory to hold exported and run the python file that will export the data.
export.py - to be run by export_data.sh to generate several csv files which contain LOST data that is ready for importing.
imp_rdy1 - directory which contains the csv files from the database 'hw' from the first round of testing.
dump - directory which contains the csv files from the database 'hw' from the second round of testing.

Usage (input_dir is the directory which will contain the csv files that were generated on export):

$ bash export_data.sh <dbname> <input_dir>


note: be sure that a database with a LOST data model has been created before exporting data.
