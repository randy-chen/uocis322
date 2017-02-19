The files in this directory implement a simple web application to take in


Files:
app.py - A Flask app to be run using python.
config.py - Logic to find and read the configuration into memory
lost_config.json - a sample configuration file
templates/
    login.html - a template for the user login page
    create_user.html - a template for the page where a new user can be created.
    dashboard.html - a template for the page that renders from a successful login.
    error.html - a template for the page that handles login and account creation errors.
    success.html - a template for the page that renders from a successful account creation.



Usage (after database cluster and database have been created):

$ cd ..
$ ./preflight.sh <dbname>
$ cd src
$ python3 app.py 

Alternate usage:

$ cd ..
$ ./preflight.sh <dbname>
$ cd $HOME/wsgi 
$ apachectl start

Open a browser on your machine and go the url http://localhost:8080 to begin interacting with the application.
