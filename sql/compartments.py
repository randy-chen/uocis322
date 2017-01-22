# assets.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def assets():

	with open('./osnap_legacy/security_compartments.csv', 'r') as csvfile:
		reader  = csv.DictReader(csvfile)


		for row in reader:
			# for row2 in reader2:
			cur.execute("insert into compartments(abbrv, comment) values (%s,%s)", (row['compartment_tag'],row['compartment_desc'],) )

			# <<need to get the descriptions of the products>>	

			# cur.execute("update assets set product_fk =  where asset_tag = %s", row['asset tag'])
			# print(row['vendor'])

	return

assets()

conn.commit()

cur.close()
conn.close()
