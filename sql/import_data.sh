# Randy Chen, CIS 322 Assignment 2 



# curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > legacy.tar.gz 
# tar -xzvf legacy.tar.gz

## now osnap_legacy is a directory of csv files in our directory.

python3      products.py $1 $2
python3        assets.py $1 $2
python3     vechicles.py $1 $2
python3    facilities.py $1 $2
python3      asset_at.py $1 $2
python3       convoys.py $1 $2
python3       used_by.py $1 $2
python3      asset_on.py $1 $2

python3         users.py $1 $2
python3         roles.py $1 $2
python3       user_is.py $1 $2
python3 user_supports.py $1 $2

python3        levels.py $1 $2
python3  compartments.py $1 $2
python3 security_tags.py $1 $2




# rm somthing


COMMENT=false
if ${COMMENT}; then
python3 insert1.py > tmp.sql # put insertion statements into sql file.

psql $1 -p $2 -f tmp.sql     

python3 insert1.py > tmp.sql 

psql $1 -p $2 -f tmp.sql 
fi
