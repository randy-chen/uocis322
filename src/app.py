from flask import Flask, render_template, request
from config import dbname, dbhost, dbport

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/rfs')
def rfs():
    if request.method=='GET' and 'login' in request.args:
        return render_template('rfs.html',data=request.args.get('login'))

    # request.form is only populated for POST messages
    #if request.method=='POST' and 'login' in request.form:
    #    return render_template('rfs.html',data=request.form['login'])
    return render_template('index.html')

@app.route('/facilities')
def facilities():
    if request.method=='GET' and 'facilities' in request.args:
        return render_template('facilities.html',data=request.args.get('facilities'))

    # request.form is only populated for POST messages
    #if request.method=='POST' and 'login' in request.form:
    #    return render_template('rfs.html',data=request.form['login'])
    return render_template('index.html')

@app.route('/transit')
def transit():
    if request.method=='GET' and 'transit' in request.args:
        return render_template('transit.html',data=request.args.get('transit'))

    # request.form is only populated for POST messages
    #if request.method=='POST' and 'login' in request.form:
    #    return render_template('rfs.html',data=request.form['login'])
    return render_template('index.html')

@app.route('/logout')
def logout():
    if request.method=='GET':
        return render_template('logout.html')

    # request.form is only populated for POST messages
    #if request.method=='POST' and 'login' in request.form:
    #    return render_template('rfs.html',data=request.form['login'])
    return render_template('index.html')


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
