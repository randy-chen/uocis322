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
			fk   = None
			desc = None	
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk = cur.fetchone()	
			if (fk != None):
				cur.execute("select description from products where products.product_pk=%s",  (fk,) ) 
				desc = cur.fetchone()
			cur.execute("insert into assets(product_fk, asset_tag, description, alt_description) values (%s,%s,%s,%s)", (fk, row['asset tag'],desc,'HQ',) )

		for row in reader2:
			fk   = None
			desc = None	
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk = cur.fetchone()	
			if (fk != None):
				cur.execute("select description from products where products.product_pk=%s",  (fk,) ) 
				desc = cur.fetchone()
			cur.execute("insert into assets(product_fk, asset_tag, description, alt_description) values (%s,%s,%s,%s)", (fk, row['asset tag'],desc,'NC',) )
		for row in reader3:
			fk   = None
			desc = None	
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk = cur.fetchone()	
			if (fk != None):
				cur.execute("select description from products where products.product_pk=%s",  (fk,) ) 
				desc = cur.fetchone()
			cur.execute("insert into assets(product_fk, asset_tag, description, alt_description) values (%s,%s,%s,%s)", (fk, row['asset tag'],desc,'SPNV',) )
		for row in reader4:
			fk   = None
			desc = None	
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk = cur.fetchone()	
			if (fk != None):
				cur.execute("select description from products where products.product_pk=%s",  (fk,) ) 
				desc = cur.fetchone()
			cur.execute("insert into assets(product_fk, asset_tag, description, alt_description) values (%s,%s,%s,%s)", (fk, row['asset tag'],desc,'DC',) )
		for row in reader5:
			fk   = None
			desc = None	
			cur.execute("select product_pk from products where products.alt_description=%s", (row['product'],) )
			fk = cur.fetchone()	
			if (fk != None):
				cur.execute("select description from products where products.product_pk=%s",  (fk,) ) 
				desc = cur.fetchone()
			cur.execute("insert into assets(product_fk, asset_tag, description, alt_description) values (%s,%s,%s,%s)", (fk, row['asset tag'],desc,'MB005') )
			# <<need to get the descriptions of the products>>	

			# print(row['vendor'])

	return

assets()

conn.commit()

cur.close()
conn.close()
