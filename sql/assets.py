# assets.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def assets():

	with open('/home/osnapdev/uocis322/sql/osnap_legacy/MB005_inventory.csv', 'r') as csvfile, open('/home/osnapdev/uocis322/sql/osnap_legacy/HQ_inventory.csv', 'r') as csv2, open('/home/osnapdev/uocis322/sql/osnap_legacy/DC_inventory.csv', 'r') as csv3, open('/home/osnapdev/uocis322/sql/osnap_legacy/NC_inventory.csv', 'r') as csv4, open('/home/osnapdev/uocis322/sql/osnap_legacy/SPNV_inventory.csv', 'r') as csv5:
		# title  = ['vendor', 'description']
		reader  = csv.DictReader(csvfile)
		reader2 = csv.DictReader(csv2)
		reader3 = csv.DictReader(csv3)
		reader4 = csv.DictReader(csv4)
		reader5 = csv.DictReader(csv5)


		for row in reader:
			# for row2 in reader2:
			cur.execute("insert into assets(asset_tag) values (%s)", (row['asset tag'],) )
		for row in reader2:
			cur.execute("insert into assets(asset_tag) values (%s)", (row['asset tag'],) )
		for row in reader3:
			cur.execute("insert into assets(asset_tag) values (%s)", (row['asset tag'],) )
		for row in reader4:
			cur.execute("insert into assets(asset_tag) values (%s)", (row['asset tag'],) )
		for row in reader5:
			cur.execute("insert into assets(asset_tag) values (%s)", (row['asset tag'],) )

			# <<need to get the descriptions of the products>>	

			# cur.execute("update assets set product_fk =  where asset_tag = %s", row['asset tag'])
			# print(row['vendor'])

	return

assets()

conn.commit()

cur.close()
conn.close()
