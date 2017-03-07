# Randy Chen, CIS 322 W'17.
#
# This is my own work. Though I would like to acknowledge:
#
# Andrew Hampton for his help on using jinja2 to generate and display tables on the webpage.

from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname, dbhost, dbport
import psycopg2, sys, json, datetime

app = Flask(__name__)
conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur  = conn.cursor()

app.secret_key = "osnapwholostderp?"


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='GET':
		session['asset_table'] = []
		session['user'] = ""
		session['role'] = ""
		return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)
	
	if request.method=='POST':
		usern = request.form['login_name']
		passw = request.form['login_pass']
		session['user'] = usern + " "
		if valid_login(usern, passw):
			session['user'] = usern
			return redirect(url_for('dashboard'))
	
	return redirect(url_for('error'))


def valid_login(_username, _password):
	cur.execute("SELECT username, password FROM users WHERE username=%s", (_username,))
	login_data = cur.fetchone()
	#print(login_data)
	if login_data!=None:
		if (login_data[0]==_username and login_data[1]==_password):
			return True
	return False
""""""
@app.route('/activate_user', methods=['POST'])
def activate_user():
	#if request.method=='GET':
	#	return render_template('create_user.html')

	if request.method=='POST':
		usern     = request.form['user']
		passw     = request.form['pass']
		form_role = request.form['role']
		if valid_input(usern, passw)==1:	
			cur.execute("INSERT INTO users (username, password, role, active) VALUES (%s, %s, %s, %s)", (usern,passw,form_role,True,))
			conn.commit()
			#session['user'] = usern
			#session['role'] = form_role
			return "User successfully activated!"

		if valid_input(usern, passw)==2:	
			cur.execute("UPDATE users SET password=%s WHERE username=%s", (passw,usern,))
			conn.commit()
			return "User password successfully updated!"

	session['user'] = ""
	return "Invalid input: be sure that the information entered is of correct length. Please try again!"
	
def valid_input(_username, _password):
	cur.execute("SELECT username FROM users WHERE username=%s", (_username,))
	existing_name = cur.fetchone()
	if (len(_username)>16 or len(_password)>16 or len(_username)==0):
		return False
	if existing_name:
		return 2
	return 1

@app.route('/revoke_user', methods=['POST'])
def revoke_user():
	#if request.method=='GET':
	#	return render_template('create_user.html')

	if request.method=='POST':
		usern     = request.form['user']
		if valid_input(usern, "revoke")==2:	
			cur.execute("DELETE FROM users WHERE username=%s", (usern,))
			conn.commit()
			#session['user'] = usern
			#session['role'] = form_role
			return "User successfully revoked! They have been obliterated from the database."

	session['user'] = ""
	return "Invalid input: be sure that the username entered exists and is of correct length. Please try again!"

@app.route('/dashboard', methods=['GET'])
def dashboard():
	session['asset_table'] = []
	session['transfer_table'] = []
	cur.execute("SELECT role FROM users WHERE username=%s", (session['user'],))
	valid_get = cur.fetchone()
	print(valid_get)
	if valid_get is None:
		return redirect(url_for('af_error'))
	user_role = cur.fetchone()[0]
	print(user_role)
	if user_role is None:
		return redirect(url_for('af_error'))
	session['role'] = user_role
	
	sql = """SELECT req_id, requester, tf_asset, src_fac, des_fac, approver 
FROM transfers 
WHERE (tf_status='Approved' 
AND unload_dt IS NULL)
"""
	# in the future, include the time that the request was made on
	cur.execute(sql)
	res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
	logistics_table = []   # this is the processed result I'll stick in the session (or pass to the template)
	for r in res:
		logistics_table.append( dict(zip(('req_id','requester', 'tf_asset', 'src_fac', 'des_fac', 'approver'), r)) )
	session['logistics_table'] = logistics_table

	sql = """SELECT req_id, requester, tf_asset, src_fac, des_fac 
FROM transfers
WHERE tf_status='Pending'
"""
	cur.execute(sql)
	res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
	facoff_table = []   # this is the processed result I'll stick in the session (or pass to the template)
	for r in res:
		facoff_table.append( dict(zip(('req_id','requester', 'tf_asset', 'src_fac', 'des_fac'), r)) )
	session['facoff_table'] = facoff_table

	return render_template('dashboard.html')

""""""	
@app.route('/add_facility', methods=['GET','POST'])
def add_facility():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('af_error'))
		sql = "SELECT common_name, fcode, location FROM facilities"
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		facility_list = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			facility_list.append( dict(zip(('common_name', 'fcode', 'location'), r)) )
		session['facilities'] = facility_list
		return render_template('facility.html')

	if request.method=='POST':
		form_name = request.form['fname']
		form_code = request.form['fcode']
		form_loca = request.form['floca']
		if valid_facility(form_name,form_code):	
			cur.execute("INSERT INTO facilities (common_name, fcode, location) VALUES (%s, %s, %s)", (form_name,form_code,form_loca,))
			conn.commit()
			return redirect(url_for('add_facility'))

	return redirect(url_for('af_error'))


def valid_facility(name, code):
	cur.execute("SELECT common_name, fcode FROM facilities WHERE (common_name=%s OR fcode=%s)", (name,code,))
	facility_data = cur.fetchone()
	#print(facility_data)
	if (facility_data or len(name)>32 or len(code)>6 or len(name)==0 or len(code)==0):
		return False
	return True
""""""
@app.route('/add_asset', methods=['GET','POST'])
def add_asset():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('af_error'))
		# Ready the data to load the assets table
		sql = """SELECT asset_tag, description, common_name, arrival, status, disposal 
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
"""
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		asset_table = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			asset_table.append( dict(zip(('asset_tag', 'description', 'common_name', 'arrival', 'status', 'disposal'), r)) )
		#print(asset_table)
		session['asset_table'] = asset_table
		
		# Ready the data for the facillities drop-down
		sql = "SELECT common_name FROM facilities"
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		facility_list = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			facility_list.append(r[0])
		session['facility_dropdown'] = facility_list
		session['num_fac'] = len(facility_list)	
	
		return render_template('add_asset.html')

	if request.method=='POST':
		tag       = request.form['tag']
		desc      = request.form['desc']
		facility  = request.form['faci']
		form_date = request.form['date']
		if not valid_date(form_date):
			return redirect(url_for('af_error'))
		timestamp = datetime.datetime.strptime(form_date, '%m/%d/%Y')
		stat = "Present"
		if valid_asset_add(tag):	
				cur.execute("INSERT INTO assets (asset_tag, description, status) VALUES (%s, %s, %s)", (tag,desc,stat,))
				conn.commit()
				cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s", (tag,))
				asset_key = cur.fetchone()
				#print(facility)
				cur.execute("SELECT facility_pk FROM facilities WHERE common_name=%s", (facility,))
				facility_key = cur.fetchone()
				#print(facility_key)
				cur.execute("INSERT INTO asset_at (asset_fk, facility_fk, arrival) VALUES (%s, %s, %s)", (asset_key,facility_key,timestamp,))
				conn.commit()
				
				return redirect(url_for('add_asset'))

	return redirect(url_for('af_error'))

def valid_asset_add(_tag):
	cur.execute("SELECT asset_tag FROM assets WHERE asset_tag=%s", (_tag,))
	asset_data = cur.fetchone()
	#print(asset_data)
	if asset_data or len(_tag)>16 or len(_tag)==0:
		return False
	return True


def valid_date(_date):
	try:
		datetime.datetime.strptime(_date, '%m/%d/%Y')
	except ValueError:
		return False
	return True
	
""""""
@app.route('/dispose_asset', methods=['GET','POST'])
def dispose_asset():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('error'))
		#print("printing role: " + session['role'])
		if session['role']=="Logistics Officer": 
			return render_template('dispose_asset.html')

	if request.method=='POST':
		form_tag  =  request.form['tag']
		form_date = request.form['disp']
		if not valid_date(form_date):
			return redirect(url_for('af_error'))
		timestamp = datetime.datetime.strptime(form_date, '%m/%d/%Y')
		if valid_disposal(form_tag, timestamp):	
			cur.execute("UPDATE assets SET status='Disposed' WHERE asset_tag=%s", (form_tag,))
			conn.commit()
			sql = """SELECT asset_pk
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE asset_tag=%s
"""
			cur.execute(sql, (form_tag,))
			asset_key = cur.fetchone()
			#print(asset_key)
			cur.execute("UPDATE asset_at SET disposal=%s WHERE asset_fk=%s", (timestamp,asset_key,))
			conn.commit()
			return redirect(url_for('dashboard'))

	return redirect(url_for('af_error'))

def valid_disposal(tag, date):
	if len(tag)>16 or len(tag)==0:
		return False
	sql = """SELECT asset_tag
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE (asset_tag=%s AND arrival<%s AND status='Present') 
"""
	tag_and_date =(tag, date,)
	cur.execute(sql, tag_and_date)
	dispose_data = cur.fetchone()
	#print(dispose_data)
	if dispose_data:
		return True
	return False
""""""
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('error'))
		# Ready the data for the facillities drop-down
		sql = "SELECT common_name FROM facilities"
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		facility_list = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			facility_list.append(r[0])
		session['facility_dropdown'] = facility_list

		return render_template('asset_report.html')

	if request.method=='POST':
		facil     = request.form['r_faci']
		rdate     = request.form['r_date']
		if not valid_date(rdate):
			return redirect(url_for('af_error'))
		timestamp = datetime.datetime.strptime(rdate, '%m/%d/%Y')
		if facil == "":
			sql = """SELECT asset_tag, description, common_name, arrival, status, disposal 
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE (arrival<=%s AND (status='Present' OR disposal>%s)) 
"""
			exe = (rdate,rdate,)
			cur.execute(sql,exe)
		else:
			sql = """SELECT asset_tag, description, common_name, arrival, status, disposal 
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE (arrival<=%s AND (status='Present' OR disposal>%s) AND common_name=%s) 
"""
			exe = (rdate,rdate,facil,)
			cur.execute(sql,exe)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		asset_table = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			asset_table.append( dict(zip(('asset_tag', 'description', 'common_name', 'arrival', 'status', 'disposal'), r)) )
		session['asset_table'] = asset_table
			
		return redirect(url_for('asset_report'))

	return redirect(url_for('af_error'))
""""""
@app.route('/transfer_req', methods=['GET','POST'])
def transfer_req():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('error'))
		#print("printing role: " + session['role'])
		if session['role']=="Logistics Officer": 
			# Ready the data to load the assets table
			sql = """SELECT asset_tag, description, fcode, arrival, status, disposal 
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE status='Present'
"""
			cur.execute(sql)
			res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			asset_table = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res:
				asset_table.append( dict(zip(('asset_tag', 'description', 'focde', 'arrival', 'status', 'disposal'), r)) )
			#print(asset_table)
			session['asset_table'] = asset_table

			# Ready the data for the present assets drop-down
			sql = "SELECT asset_tag FROM assets where status='Present'"
			cur.execute(sql)
			res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			present_asset_list = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res:
				present_asset_list.append(r[0])
			session['present_asset_dropdown'] = present_asset_list
			session['num_assets']             = len(present_asset_list)
			
			# Ready the data for the facillities drop-down
			sql = "SELECT fcode FROM facilities"
			cur.execute(sql)
			res1 = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			facility_list = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res1:
				facility_list.append(r[0])
			session['facility_dropdown'] = facility_list

			return render_template('transfer_req.html')

	if request.method=='POST':
		asset    = request.form['tag']
		dest     = request.form['dest']
		sql = """SELECT fcode
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE asset_tag=%s
"""
		cur.execute(sql, (asset,))
		source   = cur.fetchone()[0]
		print(source)
		print(dest)
		if asset==None or source==dest:
			return redirect(url_for('af_error'))

		cur.execute("INSERT INTO transfers (requester, tf_asset, src_fac, tf_status, des_fac) VALUES (%s, %s, %s, %s, %s)", (session['user'],asset,source,'Pending',dest,))
		conn.commit()# In the future, will need to track the date of the request<><><><><>
		
		return redirect(url_for('req_success'))
			
	return redirect(url_for('af_error'))
""""""
@app.route('/approve_req', methods=['GET','POST'])
def approve_req():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('error'))
		#print("printing role: " + session['role'])
		if session['role']=="Facilities Officer": 
			# Ready the data to load the requests table
			sql = """SELECT req_id, requester, tf_asset, src_fac, des_fac 
FROM transfers
WHERE tf_status='Pending'
"""
			cur.execute(sql)
			res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			request_table = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res:
				request_table.append( dict(zip(('req_id','requester', 'tf_asset', 'src_fac', 'des_fac'), r)) )
			#print(request_table)
			session['request_table'] = request_table

			# Ready the data for the requests drop-down
			sql = "SELECT req_id FROM transfers WHERE tf_status='Pending'"
			cur.execute(sql)
			res1 = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			request_list = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res1:
				request_list.append(r[0])
			session['request_dropdown'] = request_list

			return render_template('approve_req.html')

	if request.method=='POST':
		req_id = request.form['request']
		# in the future, will need to keep track of the date that the request got approved.
		if request.form['decision']=='Approve Request!':
			cur.execute("UPDATE transfers SET tf_status='Approved', approver=%s WHERE req_id=%s", (session['user'],req_id,))
			conn.commit()
			return redirect(url_for('dashboard'))
		if request.form['decision']=='Reject Request!':
			cur.execute("DELETE FROM transfers WHERE req_id=%s", (req_id,))
			conn.commit()
			return redirect(url_for('dashboard'))
		
		return redirect(url_for('af_error'))

	return redirect(url_for('af_error'))
""""""
@app.route('/update_transit', methods=['GET','POST'])
def update_transit():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('error'))
		#print("printing role: " + session['role'])
		if session['role']=="Logistics Officer": 
			# Ready the data to load the requests table
			sql = """SELECT req_id, requester, tf_asset, src_fac, load_dt, des_fac, unload_dt, approver 
FROM transfers 
WHERE (tf_status='Approved' 
AND unload_dt IS NULL)
"""
			# in the future, include the time that the request was made on
			cur.execute(sql)
			res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			request_table = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res:
				request_table.append( dict(zip(('req_id','requester', 'tf_asset', 'src_fac','load_dt', 'des_fac', 'unload_dt', 'approver'), r)) )
			#print(request_table)
			session['request_table'] = request_table

			# Ready the data for the requests drop-down
			sql = "SELECT req_id FROM transfers WHERE (tf_status='Approved' AND unload_dt IS NULL)"
			cur.execute(sql)
			res1 = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
			request_list = []   # this is the processed result I'll stick in the session (or pass to the template)
			for r in res1:
				request_list.append(r[0])
			session['request_dropdown'] = request_list
			session['num_reqs']        = len(request_list)

			return render_template('update_transit.html')

	if request.method=='POST':
		# only updates requests that have been approved.
		req_id  = request.form['request']
		up_date = request.form['u_date']
		if request.form['time']=='Set Load Time!':
			#print("loading")
			update_type = 0
			if valid_update(req_id, up_date, update_type):
				#print("doing the database updating")
				timestamp = datetime.datetime.strptime(up_date, '%m/%d/%Y')
				cur.execute("UPDATE transfers SET load_dt=%s WHERE req_id=%s", (timestamp,req_id,))
				conn.commit()
			
				return redirect(url_for('dashboard'))

		if request.form['time']=='Set Unload Time!':
			#print("unloading")
			update_type = 1
			if valid_update(req_id, up_date, update_type):			
				#print("doing the database unloading")
				timestamp = datetime.datetime.strptime(up_date, '%m/%d/%Y')
				cur.execute("UPDATE transfers SET unload_dt=%s WHERE req_id=%s", (timestamp,req_id,))
				conn.commit()

				return redirect(url_for('dashboard'))
			
		return redirect(url_for('af_error'))

	return redirect(url_for('af_error'))

def valid_update(_request, _date, _type):
	if not valid_date(_date):
		return False
	sql = """SELECT load_dt, unload_dt
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
JOIN transfers t ON a.asset_tag=t.tf_asset
WHERE (req_id=%s) 
"""
	req =(_request,)
	cur.execute(sql, req)
	load_data = cur.fetchone()
	#print(dispose_data)
	# case for load
	if _type==0 and (not load_data[0]) and (not load_data[1]):
		return True
	# case for unload
	elif _type==1 and load_data[0] and (not load_data[1]):
		timestamp = datetime.datetime.strptime(_date, '%m/%d/%Y')
		if load_data[0] < timestamp:
			return True
	
	return False
		
""""""
@app.route('/transfer_report', methods=['GET','POST'])
def transfer_report():
	if request.method=='GET':
		if session['user']=="":
			return redirect(url_for('error'))
		return render_template('transfer_report.html') 
	

	if request.method=='POST':
		tdate     = request.form['t_date']
		if not valid_date(tdate):
			return redirect(url_for('af_error'))
		timestamp = datetime.datetime.strptime(tdate, '%m/%d/%Y')
		sql = """SELECT tf_asset, load_dt, unload_dt
FROM transfers
WHERE (load_dt<%s AND (unload_dt>%s OR unload_dt IS NULL)) 
"""
		exe = (timestamp,timestamp,)
		cur.execute(sql,exe)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		transfer_table = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			transfer_table.append( dict(zip(('asset_tag', 'load_dt', 'unload_dt'), r)) )
		session['transfer_table'] = transfer_table
			
		return redirect(url_for('transfer_report'))

	return redirect(url_for('af_error'))
""""""
""""""

@app.route('/success')
def success():
	if session['user']=="":
		return redirect(url_for('error'))
	return render_template('success.html') 

@app.route('/req_success')
def req_success():
	if session['user']=="":
		return redirect(url_for('error'))
	return render_template('req_success.html') 

@app.route('/error')
def error():
	return render_template('error.html') 

@app.route('/af_error')
def af_error():
	return render_template('af_error.html') 

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
