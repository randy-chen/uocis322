
# Thanks to Andrew Hampton for the starter code.

import psycopg2
import csv

def products():

	with open('/home/uocis322/sql/osnap_legacy/products_list.csv', 'r') as csvfile, open('/home/uocis322/sql/products.csv', 'w') as outfile:
		title  = ['vendor', 'description']
		reader = csv.DictReader(csvfile)
		writer = csv.DictWriter(outfile, fieldnames=title)
		writer.writeheader()
		
		for row in reader:
			writer.writerow({'vendor':row['vendor'], 'description':row['description']})

	return

products()
