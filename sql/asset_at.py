# asset_at.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def asset_at():

	with open('./osnap_legacy/transit.csv', 'r') as csvfile: #, open('./osnap_legacy/N.csv', 'r') as csv2, open('./osnap_legacy/SPNV_inventory.csv', 'r') as csv3, open('./osnap_legacy/DC_inventory.csv', 'r') as csv4, open('./osnap_legacy/MB005_inventory.csv', 'r') as csv5:
		reader  = csv.DictReader(csvfile)
		'''reader2 = csv.DictReader(csv2)
		reader3 = csv.DictReader(csv3)
		reader4 = csv.DictReader(csv4)
		reader5 = csv.DictReader(csv5)
		'''

		for i in range(16):
			afk    = None
			ffk    = None
			arrive = None	
			depart = None
			if (i < 4):
				cur.execute("select asset_pk from assets where assets.alt_description=%s", ('MB005',) )
				afk    = cur.fetchone()	
				cur.execute("select facility_pk from facilities where facilities.fcode=%s", ('MB005',) )
				ffk    = cur.fetchone()	
				arrive = '1/4/2017'	
				depart = ''	
				cur.execute("insert into asset_at(asset_fk, facility_fk, arrive_dt, depart_dt) values (%s,%s,%s,%s)", (afk,ffk,arrive,depart,) )

			# <<need to get the descriptions of the products>>	

			# print(row['vendor'])

	return

asset_at()

conn.commit()

cur.close()
conn.close()
