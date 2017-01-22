# Thanks to Andrew Hampton for the starter code.

import csv

def products():

	with open('/home/osnapdev/uocis322/sql/osnap_legacy/product_list.csv', 'r') as csvfile, open('/home/osnapdev/uocis322/sql/osnap_legacy/products.csv', 'w') as outfile:
		title  = ['vendor', 'description']
		reader = csv.DictReader(csvfile)
		writer = csv.DictWriter(outfile, fieldnames=title)
		writer.writerheader()
		
		for row in reader:
			writer.writerow({'vendor':row['vendor'], 'description':row['description']})

	return

products()
