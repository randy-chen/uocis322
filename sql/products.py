# products.py. Thanks to Andrew Hampton for the starter code.

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def products():

	with open('/home/osnapdev/uocis322/sql/osnap_legacy/product_list.csv', 'r') as csvfile:
		title  = ['vendor', 'description']
		reader = csv.DictReader(csvfile)
		# writer = csv.DictWriter(outfile, fieldnames=title)
		# writer.writeheader()
		for row in reader:
			cur.execute("insert into products(vendor, description) values (%s, %s)", (row['vendor'], row['description'],) )
			# cur.execute("insert into products(dscription) values ('description:row['description']) ;")	
			# writer.writerow({'vendor':row['vendor'], 'description':row['description']})
			print(row['vendor'])
			var = 0	

	return

products()

conn.commit()

cur.close()
conn.close()
