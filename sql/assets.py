# assets.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def assets():

	with open('/home/osnapdev/uocis322/sql/osnap_legacy/MB005_inventory.csv', 'r') as csvfile:
		# title  = ['vendor', 'description']
		reader = csv.DictReader(csvfile)
		

		for row in reader:
			cur.execute("insert into assets(asset_tag, description) values (%s, %s)", (row['asset tag'], row['description'],) )
			# cur.execute("update assets set product_fk =  where asset_tag = %s", row['asset tag'])
			# print(row['vendor'])

	return

assets()

conn.commit()

cur.close()
conn.close()
