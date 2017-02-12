from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import psycopg2, sys, json

app = Flask(__name__)
conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur  = conn.cursor()


@app.route('/')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/rest')
def rest():
	return render_template('rest.html')

@app.route('/rest/lost_key', methods=('POST',))
def lost_key():
	#if request.method=='POST' and 'arguments' in request.form:
		#print(request.form['arguments'], '\nprinted')
		#req=json.loads(request.form['arguments'])	

	dat = dict()
	dat['timestamp'] = '13'	
	dat['result'] = 'OK'
	dat['key'] = 'Im_excited_for_the_next_half_of_the_term!'	
	data = json.dumps(dat)
	
	return data

@app.route('/rest/activate_user', methods=('POST',))
def activate_user():
	if request.method=='POST' and 'arguments' in request.form:
		req=json.loads(request.form['arguments'])	
	
	dat = dict()
	dat['timestamp'] = req['timestamp']	
	dat['result'] = 'OK'
	data = json.dumps(dat)
	return data

@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
	if request.method=='POST' and 'arguments' in request.form:
		req=json.loads(request.form['arguments'])	

	dat = dict()
	dat['timestamp'] =  req['timestamp']	
	dat['result'] = 'OK'
	data = json.dumps(dat)
	
	return data

@app.route('/rest/list_products', methods=('POST',))
def list_products():
    """This function was written entirely by the instructor
    """
    # Check maybe process as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    # Unmatched, take the user somewhere else
    else:
        redirect('rest')
    
    # Setup a connection to the database
    conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
    cur  = conn.cursor()
    
    # If execution gets here we have request json to work with
    # Do I need to handle compartments in this query?
    if len(req['compartments'])==0:
        print("have not compartment")
        # Just handle vendor and description
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from products p
left join security_tags t on p.product_pk=t.product_fk
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description"
            cur.execute(SQLstart)
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s and vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],req['vendor']))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " where description ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['description'],))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " where vendor ilike %s group by vendor,description"
                cur.execute(SQLstart,(req['vendor'],))
    else:
        print("have compartment %s"%len(req['compartments']))
        # Need to handle compartments too
        SQLstart = """select vendor,description,string_agg(c.abbrv||':'||l.abbrv,',')
from security_tags t
left join sec_compartments c on t.compartment_fk=c.compartment_pk
left join sec_levels l on t.level_fk=l.level_pk
left join products p on t.product_fk=p.product_pk
where product_fk is not NULL and c.abbrv||':'||l.abbrv = ANY(%s)"""
        if req['vendor']=='' and req['description']=='':
            # No filters, add the group by and query is ready to go
            SQLstart += " group by vendor,description,product_fk having count(*)=%s"
            cur.execute(SQLstart,(req['compartments'],len(req['compartments'])))
        else:
            if not req['vendor']=='' and not req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],req['vendor'],len(req['compartments'])))
            elif req['vendor']=='':
                req['description']="%"+req['description']+"%"
                SQLstart += " and description ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['description'],len(req['compartments'])))
            elif req['description']=='':
                req['vendor']="%"+req['vendor']+"%"
                SQLstart += " and vendor ilike %s group by vendor,description,product_fk having count(*)=%s"
                cur.execute(SQLstart,(req['compartments'],req['vendor'],len(req['compartments'])))
    
    # One of the 8 cases should've run... process the results
    dbres = cur.fetchall()
    listing = list()
    for row in dbres:
        e = dict()
        e['vendor'] = row[0]
        e['description'] = row[1]
        if row[2] is None:
            e['compartments'] = list()
        else:
            e['compartments'] = row[2].split(',')
        listing.append(e)
    
    # Prepare the response
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['listing'] = listing
    data = json.dumps(dat)
    
    conn.close()
    return data

@app.route('/rest/add_product', methods=('POST',))
def add_product():
	if request.method=='POST' and 'arguments' in request.form:
		req=json.loads(request.form['arguments'])	

	dat = dict()
	dat['timestamp'] =  req['timestamp']
	dat['result'] = 'OK'
	data = json.dumps(dat)
		
	return data

@app.route('/rest/add_asset', methods=('POST',))
def add_asset():
	if request.method=='POST' and 'arguments' in request.form:
		req=json.loads(request.form['arguments'])	
	
	dat = dict()
	dat['timestamp'] =  req['timestamp']	
	dat['result'] = 'OK'
	data = json.dumps(dat)
	
	return data

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
