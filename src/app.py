from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname, dbhost, dbport
import psycopg2, sys, json

app = Flask(__name__)
conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur  = conn.cursor()

app.secret_key = "onsapwhoderp?"

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method=='GET':
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

#session['db'] = dbname

def valid_login(_username, _password):
	cur.execute("SELECT username, password FROM users WHERE username=%s", (_username,))
	login_data = cur.fetchone()
	#print(login_data)
	if login_data!=None:
		if (login_data[0]==_username and login_data[1]==_password):
			return True
	return False

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
			session['role'] = form_role
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
		sql = "SELECT asset_tag, description, status FROM assets"
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		asset_table = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			asset_table.append( dict(zip(('asset_tag', 'description', 'status'), r)) )
		session['asset_table'] = asset_table
		
		# Ready the data for the facillities drop-down
		sql = "SELECT common_name FROM facilities"
		cur.execute(sql)
		res = cur.fetchall()  # this is the result of the database query "SELECT column_name1, column_name2 FROM some_table"
		facility_list = []   # this is the processed result I'll stick in the session (or pass to the template)
		for r in res:
			facility_list.append( dict(zip(('common_name'), r)) )
		session['facility_dropdown'] = facility_list
		return render_template('add_asset.html')

	if request.method=='POST':
		tag  = request.form['tag']
		desc = request.form['desc']
		stat = "Present"
		#if valid_input(usern, passw):	
		cur.execute("INSERT INTO assets (username, password, role) VALUES (%s, %s, %s)", (usern,passw,form_role,))
		conn.commit()
		return redirect(url_for('add_asset'))

	session['user'] = ""
	return redirect(url_for('error'))

def valid_asset_add(_username, _password):
	cur.execute("SELECT username, password FROM users WHERE username=%s", (_username,))
	login_data = cur.fetchone()
	print(login_data)
	if login_data!=None:
		if (login_data[0]==_username and login_data[1]==_password):
			return True
	return False
""""""
@app.route('/dispose_asset', methods=['GET','POST'])
def dispose_asset():
	if request.method=='GET':
		if session['role']== "Logistics Officer":: 
			return render_template('dispose_asset.html')

	if request.method=='POST':
		form_tag  =  request.form['tag']
		form_date = request.form['disp']
		if valid_disposal(form_tag, form_date):	
			#cur.execute("UPDATE users (username, password, role) VALUES (%s, %s, %s)", (usern,passw,form_role,))
			#conn.commit()
			return redirect(url_for('dispose_asset'))

	return redirect(url_for('error'))

def valid_dispose(tag, date):
	sql = """SELECT asset_tag
FROM assets a
JOIN asset_at aa on a.asset_pk=aa.asset_fk
JOIN facilities f on aa.facility_fk=f.facility_pk
WHERE (asset_tag=%s AND 
"""
	tag_and_date =((),)
	cur.execute("SELECT asset_tag FROM asset_at WHERE (asset_tag=%s AND ", (_username,))
	login_data = cur.fetchone()
	print(login_data)
	if login_data!=None:
		if (login_data[0]==_username and login_data[1]==_password):
			return True
	return False
""""""
@app.route('/asset_report', methods=['GET','POST'])
def asset_report():
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
			return redirect(url_for('success'))

	session['user'] = ""
	return redirect(url_for('error'))
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
