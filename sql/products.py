# products.py. Thanks to Andrew Hampton for the starter code.

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor() 

def products():

	with open('./osnap_legacy/product_list.csv', 'r') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			cur.execute("insert into products(vendor, description, alt_description) values (%s,%s,%s)", (row['vendor'], row['description'], row['name'],) )

	return

products()

conn.commit()

cur.close()
conn.close()
