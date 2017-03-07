# Much of the code in this file was provided by the instructor.

# This client can be used to interact with the LOST interface prior to encryption
# implementation

import sys
import json
import datetime

# URL lib parts
from urllib.request import Request, urlopen
from urllib.parse   import urlencode

def main():
	# Check the CLI arguments
	if len(sys.argv)<5 :
		print("Usage: python3 %s <url> <username> <password> <role>"%sys.argv[0])
		return

	# Prep the arguments blob
	args = dict()
	args['user']  = sys.argv[2]
	args['pass']  = sys.argv[3]
	if sys.argv[4]!='facofc' and sys.argv[4]!='logofc':
		print("Role entered was invalid. Must specify either 'facofc' or 'logofc'")
		return
	if sys.argv[4]=='facofc':	
		args['role']  = 'Facilities Officer'
	if sys.argv[4]=='logofc':
		args['role']  = 'Logistics Officer'

	# Print a message to let the user know what is being tried
	print("Activating user: %s"%args['user'])

	# Setup the data to send
	data = urlencode(args)
	#print("sending:\n%s"%data)

	# Make the resquest
	re_route = "activate_user" # first maybe try create_user
	req = Request(sys.argv[1]+re_route,data.encode('ascii'),method='POST')

	# response from webserver. Maybe in app.py return a string about success.
	res = urlopen(req)
	result = str(res.read())[1:]

	# Print the result code
	print("Call to LOST returned: %s"%result)


if __name__=='__main__':
	main()
