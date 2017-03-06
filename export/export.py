import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur  = conn.cursor()
fks  = dict()

def export():

	with open('users.csv', 'w') as csvfile, open('facilities.csv', 'w') as csvfile1, open('assets.csv', 'w') as csvfile2, open('transfers.csv', 'w') as csvfile3:
		fieldnames  = ['username', 'password', 'role', 'active']
		fieldnames1 = ['fcode', 'common_name']
		fieldnames2 = ['asset_tag', 'description', 'facility', 'acquired', 'disposed']
		fieldnames3 = ['asset_tag','request_by','request_dt','approve_by','approve_dt','source','destination','load_dt','unload_dt']
		writer  = csv.DictWriter(csvfile,   fieldnames=fieldnames)
		writer1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
		writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames2)
		writer3 = csv.DictWriter(csvfile3, fieldnames=fieldnames3)
# users
		cur.execute("SELECT username, password, role, active FROM users")
		rows = cur.fetchall()
		writer.writeheader()
		for row in rows:
			writer.writerow({'username': row[0], 'password': row[1], 'role': row[2], 'active': row[3]})
# facilities
		cur.execute("SELECT fcode, common_name FROM facilities")
		rows = cur.fetchall()
		writer1.writeheader()
		for row in rows:
			#print(row)
			writer1.writerow({'fcode': row[0], 'common_name': row[1]})
# assets
		sql = """SELECT asset_tag, description, fcode, arrival, disposal
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
"""
		cur.execute(sql)
		rows = cur.fetchall()
		writer2.writeheader()
		for row in rows:
			writer2.writerow({'asset_tag': row[0], 'description': row[1], 'facility': row[2], 'acquired': row[3], 'disposed': row[4]})
# transfers
		cur.execute("SELECT tf_asset,requester,req_dt,approver,aprv_dt,src_fac,des_fac,load_dt,unload_dt FROM transfers")
		rows = cur.fetchall()
		writer3.writeheader()
		for row in rows:
			writer3.writerow({'asset_tag': row[0], 'request_by': row[1], 'request_dt': row[2], 'approve_by': row[3], 'approve_dt': row[4],'source': row[5],'destination': row[6],'load_dt': row[7],'unload_dt': row[8]})


export()

conn.commit()

cur.close()
conn.close()
