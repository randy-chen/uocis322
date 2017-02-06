The files in this directory implement a simple web application to take in

The form on the login page submits to the Report Filters page, which lets the user generate reports on facilities and assets as well as which assets are in transit. There is also a logout page which can be reached from either report page and the filters page. From the logout screen, the user can go back to the login screen, which will take them to the filters page, where they can generate and view more reports if they wish. 

Files:
app.py - A Flask app to be run using python.
config.py - Logic to find and read the configuration into memory
lost_config.json - a sample configuration file
templates/
    login.html - a template for the user login page
    rfs.html - a template for page where the user can filter and generate reports
    facilities.html - a template for the Facility Inventory Report page
    transit.html - a template for the In Transit Report page
    logout.html - a template for the logout page



Usage (after database cluster and database have been created):

$ cd ..
$ ./preflight.sh <dbname>
$ cd src
$ python3 app.py 

Open a browser on your machine and go the url http://localhost:8080 to begin interacting with the application.
