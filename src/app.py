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
		return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)
	
	if request.method=='POST':
		usern = request.form['login_name']
		passw = request.form['login_pass']
		session['user'] = usern + " "
		if valid_login(usern, passw):
			session['user'] = usern
			return redirect(url_for('dashboard'))
	
	return redirect(url_for('error'))


@app.route('/create_user', methods=['GET','POST'])
def create_user():
	if request.method=='GET':
		return render_template('create_user.html')

	if request.method=='POST':
		usern = request.form['user']
		passw = request.form['pass']
		if valid_input(usern, passw):	
			cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (usern,passw,))
			conn.commit()
			session['user'] = usern
			return redirect(url_for('success'))

	session['user'] = ""
	return redirect(url_for('error'))
	
@app.route('/dashboard', methods=['GET'])
def dashboard():
	return render_template('dashboard.html')

def valid_input(_username, _password):
	cur.execute("SELECT username FROM users WHERE username=%s", (_username,))
	existing_name = cur.fetchone()
	if (existing_name or len(_username)>16 or len(_password)>16 or len(_username)==0):
		return False
	return True

def valid_login(_username, _password):
	cur.execute("SELECT username, password FROM users WHERE username=%s", (_username,))
	login_data = cur.fetchone()
	print(login_data)
	if login_data!=None:
		if (login_data[0]==_username and login_data[1]==_password):
			return True
	return False
	
@app.route('/success')
def success():
	return render_template('success.html') 

@app.route('/error')
def error():
	return render_template('error.html') 


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
