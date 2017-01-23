This directory holds some tools for configuring the LOST database and migrating legacy OSNAP data.

Files:
README.txt - This readme file
create_tables.sql - A script to generate the base tables
products.py - Python script to insert data into the products table in the database.
assets.py - Python script to insert data into the assets table in the database.
facilities.py - Python script to insert data into the facilities table in the database.
asset_at.py - Python script to insert data into the asset_at table in the database.
import_data.sh - A script to import some data into the base tables through running the above Python scripts.

Usage (while in directory): bash import_data.sh <dbname> <portnumber> 
