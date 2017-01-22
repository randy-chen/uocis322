# assets.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()
fks  = dict()

def assets():

	with open('./osnap_legacy/HQ_inventory.csv', 'r') as csvfile, open('./osnap_legacy/NC_inventory.csv', 'r') as csv2, open('./osnap_legacy/SPNV_inventory.csv', 'r') as csv3, open('./osnap_legacy/DC_inventory.csv', 'r') as csv4, open('./osnap_legacy/MB005_inventory.csv', 'r') as csv5:
		reader  = csv.DictReader(csvfile)
		reader2 = csv.DictReader(csv2)
		reader3 = csv.DictReader(csv3)
		reader4 = csv.DictReader(csv4)
		reader5 = csv.DictReader(csv5)

		for row in reader:
			fk   = none
            desc = none
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk   = cur.fetchone()[0]
			cur.execute("select description from products where products.alt_description=%s",  (fk,) ) 
			desc = cur.fetchone()[0]
			cur.execute("insert into assets(product_fk, asset_tag, description) values (%s,%s,%s)", (fk, row['asset tag'],desc,) )

		for row in reader2:
			fk   = none
            desc = none
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk   = cur.fetchone()[0]
			cur.execute("select description from products where products.alt_description=%s", (fk,) ) 
			desc = cur.fetchone()[0]
			cur.execute("insert into assets(product_fk, asset_tag, description) values (%s,%s,%s)", (fk, row['asset tag'],desc,) )
		for row in reader3:
			fk   = none
            desc = none
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk   = cur.fetchone()[0]
			cur.execute("select description from products where products.alt_description=%s", (fk,) ) 
			desc = cur.fetchone()[0]
			cur.execute("insert into assets(product_fk, asset_tag, description) values (%s,%s,%s)", (fk, row['asset tag'],desc,) )
		for row in reader4:
			fk   = none
            desc = none
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk   = cur.fetchone()[0]
			cur.execute("select description from products where products.alt_description=%s", (fk,) ) 
			desc = cur.fetchone()[0]
			cur.execute("insert into assets(product_fk, asset_tag, description) values (%s,%s,%s)", (fk, row['asset tag'],desc,) )
		for row in reader5:
			fk   = none
            desc = none
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk   = cur.fetchone()[0]
			cur.execute("select description from products where products.alt_description=%s", (fk,) ) 
			desc = cur.fetchone()[0]
			cur.execute("insert into assets(product_fk, asset_tag, description) values (%s,%s,%s)", (fk, row['asset tag'],desc,) )
		'''
		for row in reader3:
			cur.execute("insert into assets(product_fk, asset_tag) values (%s, %s)", ((select product_pk from products where description=row['product']),row['asset tag'],) )
		for row in reader3:

		for row in reader4:
			cur.execute("insert into assets(product_fk, asset_tag) values (%s, %s)", ((select product_pk from products where description=row['product']),row['asset tag'],) )
		for row in reader4:

		for row in reader5:
			cur.execute("insert into assets(product_fk, asset_tag) values (%s,%s)", ((select product_pk from products where description=row['product']),row['asset tag'],) )
		for row in reader5:'''
			# <<need to get the descriptions of the products>>	

			# cur.execute("update assets set product_fk =  where asset_tag = %s", row['asset tag'])
			# print(row['vendor'])

	return

assets()

conn.commit()

cur.close()
conn.close()
