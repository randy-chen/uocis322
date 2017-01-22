# Randy Chen, CIS 322 Assignment 2 

# database = $1
# portnum  = $2

# curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy.tar.gz 
# tar -xzvf legacy.tar.gz

## now osnap_legacy is a directory of csv files in our directory.
# use psql to import everything into the database??
# waiwaiwait, what about the "psql -c "COPY tbname FROM 'PATH/products.csv' delimiter ......" " ????

python3 insert1.py > tmp.sql # put insertion statements into sql file.

psql $1 -p $2 -f tmp.sql     

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 

