from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import psycopg2, sys

app = Flask(__name__)
conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur  = conn.cursor()


@app.route('/')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/rfs')
def rfs():
    if request.method=='GET' and 'login' in request.args:
        return render_template('rfs.html',data=request.args.get('login'))

    # request.form is only populated for POST messages
    #if request.method=='POST' and 'login' in request.form:
    #    return render_template('rfs.html',data=request.form['login'])
    return render_template('login.html')

@app.route('/facilities')
def facilities():

	if request.method=='GET' and 'facilities' in request.args:
		sql = """select fcode, asset_tag, arrive_dt, depart_dt
from assets a
join asset_at aa on a.asset_pk=aa.asset_fk
join facilities f on aa.facility_fk=f.facility_pk
where f.fcode=%s """
		location = (request.args.get('facilities'),)
		cur.execute(sql, location)
		res = cur.fetchall()
		table = []
		for row in res:
			table.append( dict(zip(('fcode', 'asset_tag', 'arrive_dt', 'depart_dt'), row)) )
		session['report'] = table

		return render_template('facilities.html',data=request.args.get('facilities'))

	if request.method=='GET' and 'date' in request.args:
		sql = """select fcode, asset_tag, arrive_dt, depart_dt
from assets a
join asset_at aa on a.asset_pk=aa.asset_fk
join facilities f on aa.facility_fk=f.facility_pk
where aa.arrive_dt < %s and (aa.depart_dt is NULL or aa.depart_dt > %s) """
		arrive_time = (request.args.get('date'), request.args.get('date'),)
		cur.execute(sql, arrive_time)
		res = cur.fetchall()
		table = []
		for row in res:
			table.append( dict(zip(('fcode', 'asset_tag', 'arrive_dt', 'depart_dt'), row)) )
		session['report'] = table

		return render_template('facilities.html',data=request.args.get('date'))


	return render_template('login.html')

@app.route('/transit')
def transit():
	sql = """select request_id, asset_tag, load_dt, unload_dt
from assets a
join asset_on aa on a.asset_pk=aa.asset_fk
join convoys c on aa.convoy_fk=c.convoy_pk
where aa.load_dt < %s and (aa.unload_dt is NULL or aa.unload_dt > %s) """
	load_time = (request.args.get('transit'), request.args.get('transit'),)
	cur.execute(sql, load_time)
	res = cur.fetchall()
	table = []
	for row in res:
		table.append( dict(zip(('request_id', 'asset_tag', 'load_dt', 'unload_dt'), row)) )
	session['report'] = table
	
	if request.method=='GET' and 'transit' in request.args:
		return render_template('transit.html',data=request.args.get('transit'))

	return render_template('login.html')

@app.route('/logout')
def logout():
	if request.method=='GET':
		return render_template('logout.html')

	return render_template('login.html')


if __name__ == "__main__":
	app.secret_key = "onsapwhoderp?"
	app.run(host='0.0.0.0', port=8080)
