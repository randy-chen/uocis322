import psycopg2
import csv
import sys

# need to set the psycopg2 ocnnection through the config file???


conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur  = conn.cursor()
fks  = dict()
path = sys.argv[2]
def assets():

	with open(path+'/users.csv', 'r') as csv0, open(path+'/facilities.csv', 'r') as csv1, open(path+'/assets.csv', 'r') as csv2, open(path+'/transfers.csv', 'r') as csv3:
		reader  = csv.DictReader(csv0)
		reader1 = csv.DictReader(csv1)
		reader2 = csv.DictReader(csv2)
		reader3 = csv.DictReader(csv3)

		for row in reader:
			_active = row['active']
			if _active=='' or _active=='NULL':
				_active = True
			cur.execute("INSERT INTO users(username, password, role, active) values (%s,%s,%s,%s)", (row['username'],row['password'],row['role'],_active,))
		for row in reader1:
			cur.execute("INSERT INTO facilities(fcode, common_name) values (%s,%s)", (row['fcode'],row['common_name'],))
		for row in reader2:
			cur.execute("INSERT INTO assets(asset_tag, description) values (%s,%s)", (row['asset_tag'],row['description'],))
			cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s", (row['asset_tag'],))
			asset_key = cur.fetchone()
			#print(facility)
			cur.execute("SELECT facility_pk FROM facilities WHERE fcode=%s", (row['facility'],))
			facility_key = cur.fetchone()
			#print(facility_key)
			arrv = row['acquired']
			if not arrv or arrv=='NULL':
				arrv = None
			disp = row['disposed']
			#print(disp)
			if not disp or disp=='NULL':
				disp = None
			#print("new disp val: %s", disp)
			cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrival, disposal) VALUES (%s,%s,%s,%s)", (asset_key,facility_key,arrv,disp,))
		for row in reader3:
			r_dt = row['request_dt']
			if r_dt=='':
				r_dt = None
			a_dt = row['approve_dt']
			if a_dt=='':
				a_dt = None
			l_dt = row['load_dt']
			if l_dt=='':
				l_dt = None
			u_dt = row['unload_dt']
			if u_dt=='':
				u_dt = None
			cur.execute("INSERT INTO transfers(tf_asset, requester, req_dt, approver, aprv_dt, src_fac, des_fac, load_dt, unload_dt) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (row['asset_tag'],row['request_by'],r_dt,row['approve_by'],a_dt,row['source'],row['destination'],l_dt,u_dt,))

	return

assets()

conn.commit()

cur.close()
conn.close()
