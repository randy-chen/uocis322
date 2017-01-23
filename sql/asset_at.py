# asset_at.py

import psycopg2
import csv
import sys


conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def asset_at():

	with open('./osnap_legacy/transit.csv', 'r') as csvfile, open('./osnap_legacy/MB005_inventory.csv', 'r') as csv2: 

		reader  = csv.DictReader(csvfile)
		reader2 = csv.DictReader(csv2)
		'''row1 = []
		row2 = []
		row3 = []'''
		entriesaslist = []

		i = 0
		for row in reader:
			#print(row['asset tag'])
			#print(entriesaslist)
			if (i == 0):
				entriesaslist = entriesaslist + row['asset tag'].split(', ')
			if (i == 1):
				entriesaslist = entriesaslist + row['asset tag'].split(', ')
			if (i == 2):
				entriesaslist = entriesaslist + row['asset tag'].split(', ')
			if (i > 2):
				entriesaslist.append(row['asset tag'])
			i = i + 1
		#print(entriesaslist)
		for i in range(14):
			afk    = None
			ffk    = None
			arrive = None	
			depart = None
			if (i < 4):
				#print(entriesaslist[i])
				cur.execute("select asset_pk from assets where assets.asset_tag=%s", (entriesaslist[i],) )
				afk    = cur.fetchone()	
				cur.execute("select facility_pk from facilities where facilities.fcode=%s", ('HQ',) )
				ffk    = cur.fetchone()	
				arrive = '1/7/2017'	
				depart = '1/4/2017'	
				cur.execute("insert into asset_at(asset_fk, facility_fk, arrive_dt, depart_dt) values (%s,%s,%s,%s)", (afk,ffk,arrive,depart,) )
			if (i >= 4 and i < 8):	
				cur.execute("select asset_pk from assets where assets.asset_tag=%s", (entriesaslist[i],) )
				afk    = cur.fetchone()	
				cur.execute("select facility_pk from facilities where facilities.fcode=%s", ('NC',) )
				ffk    = cur.fetchone()	
				arrive = '1/8/2017'	
				depart = '1/8/2017'	
				cur.execute("insert into asset_at(asset_fk, facility_fk, arrive_dt, depart_dt) values (%s,%s,%s,%s)", (afk,ffk,arrive,depart,) )
			if (i >= 8 and i < 10):
				cur.execute("select asset_pk from assets where assets.asset_tag=%s", (entriesaslist[i],) )
				afk    = cur.fetchone()	
				cur.execute("select facility_pk from facilities where facilities.fcode=%s", ('MB005',) )
				ffk    = cur.fetchone()	
				arrive = '1/8/2017'	
				depart = '1/8/2017'	
				cur.execute("insert into asset_at(asset_fk, facility_fk, arrive_dt, depart_dt) values (%s,%s,%s,%s)", (afk,ffk,arrive,depart,) )
			elif (i >= 10):
				cur.execute("select asset_pk from assets where assets.asset_tag=%s", (entriesaslist[i],) )
				afk    = cur.fetchone()	
				cur.execute("select facility_pk from facilities where facilities.fcode=%s", ('DC',) )
				ffk    = cur.fetchone()	
				arrive = '1/10/2017'	
				depart = '1/10/2017'	
				cur.execute("insert into asset_at(asset_fk, facility_fk, arrive_dt, depart_dt) values (%s,%s,%s,%s)", (afk,ffk,arrive,depart,) )
		for row in reader2:
			cur.execute("select asset_pk from assets where assets.asset_tag=%s", (row['asset tag'],) )
			afk    = cur.fetchone()	
			cur.execute("select facility_pk from facilities where facilities.fcode=%s", ('MB005',) )
			ffk    = cur.fetchone()	
			cur.execute("insert into asset_at(asset_fk, facility_fk) values (%s,%s)", (afk,ffk) )
			
	return

asset_at()

conn.commit()

cur.close()
conn.close()
