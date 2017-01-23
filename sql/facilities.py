# facilities.py

import psycopg2
import csv
import sys

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=int(sys.argv[2]))
cur  = conn.cursor()

def facilities():

	# cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('ST','Site 300','',) )
	# cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('LA','Los Alamos', 'New Mexico',) )
	# cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('GL','Groom Lake','',) )
	cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('HQ','Headquarters','',) )
	cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('NC','National City','California',) )
	cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('SPNV','Sparks','Nevada',) )
	cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('DC','Washington','D.C.',) )
	cur.execute("insert into facilities(fcode, common_name, location) values (%s,%s,%s)", ('MB005','','',) )

	return

facilities()

conn.commit()

cur.close()
conn.close()
