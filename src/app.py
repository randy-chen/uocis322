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

app.secret_key = "onsapwhoderp?"


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
@app.route('/create_user', methods=['GET','POST'])
def create_user():
	if request.method=='GET':
		return render_template('create_user.html')

	if request.method=='POST':
		usern     = request.form['user']
		passw     = request.form['pass']
		form_role = request.form['role']
		if valid_input(usern, passw):	
			cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (usern,passw,form_role,))
			conn.commit()
			session['user'] = usern
			#session['role'] = form_role
			return redirect(url_for('success'))

	session['user'] = ""
	return redirect(url_for('error'))
	
def valid_input(_username, _password):
	cur.execute("SELECT username FROM users WHERE username=%s", (_username,))
	existing_name = cur.fetchone()
	if (existing_name or len(_username)>16 or len(_password)>16 or len(_username)==0):
		return False
	return True

@app.route('/dashboard', methods=['GET'])
def dashboard():
	session['asset_table'] = []
	cur.execute("SELECT role FROM users WHERE username=%s", (session['user'],))
	user_role = cur.fetchone()[0]
	session['role'] = user_role
	return render_template('dashboard.html')

""""""	
@app.route('/add_facility', methods=['GET','POST'])
def add_facility():
	if request.method=='GET':
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
		print(asset_table)
		session['asset_table'] = asset_table
		
		# Ready the data for the facillities drop-down
		sql = "SELECT common_name FROM facilities"
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		facility_list = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			facility_list.append(r[0])
		session['facility_dropdown'] = facility_list
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
		print("printing role: " + session['role'])
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
			#need selection here
			sql = """SELECT asset_pk
FROM assets a
JOIN asset_at aa ON a.asset_pk=aa.asset_fk
JOIN facilities f ON aa.facility_fk=f.facility_pk
WHERE asset_tag=%s
"""
			cur.execute(sql, (form_tag,))
			asset_key = cur.fetchone()
			print(asset_key)
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
WHERE (asset_tag=%s AND arrival<=%s AND status='Present') 
"""
	tag_and_date =(tag, date,)
	cur.execute(sql, tag_and_date)
	dispose_data = cur.fetchone()
	print(dispose_data)
	if dispose_data:
		return True
	return False
""""""
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
	if request.method=='GET':
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

@app.route('/success')
def success():
	return render_template('success.html') 

@app.route('/error')
def error():
	return render_template('error.html') 

@app.route('/af_error')
def af_error():
	return render_template('af_error.html') 

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
