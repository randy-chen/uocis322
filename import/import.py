import psycopg2
import csv
import sys

# need to set the psycopg2 ocnnection through the config file???


conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()
fks  = dict()

def assets():

	with open('./osnap_legacy/users.csv', 'r') as csv0, open('./osnap_legacy/facilities.csv', 'r') as csv2, open('./osnap_legacy/assets.csv', 'r') as csv3, open('./osnap_legacy/transfers.csv', 'r') as csv4:
		reader  = csv.DictReader(csv0)
		reader1 = csv.DictReader(csv1)
		reader2 = csv.DictReader(csv2)
		reader3 = csv.DictReader(csv3)

		for row in reader:
			cur.execute("insert into users(username, password, role) values (%s,%s,%s)", (row['username'],row['password'],row['role'],)
		for row in reader1:
			cur.execute("insert into assets(asset_pk, username, password, role) values (%s,%s,%s,%s)", (row['user_pk'],row['username'],row['password'],row['role'],)
		for row in reader2:
			cur.execute("insert into users(user_pk, username, password, role) values (%s,%s,%s,%s)", (row['user_pk'],row['username'],row['password'],row['role'],)
		for row in reader3:
			cur.execute("insert into assets(product_fk, asset_tag, description, alt_description) values (%s,%s,%s,%s)", (fk, row['asset tag'],desc,'DC',) )

	return

assets()

conn.commit()

cur.close()
conn.close()
