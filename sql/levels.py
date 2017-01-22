# assets.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def assets():

	with open('./osnap_legacy/security_levels.csv', 'r') as csvfile:
		reader  = csv.DictReader(csvfile)

		for row in reader:
			cur.execute("insert into levels(abbrv, comment) values (%s,%s)", (row['level'],row['description']) )

	return

assets()

conn.commit()

cur.close()
conn.close()
