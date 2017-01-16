# Randy Chen, CIS 322 Assignment 1.

git clone https://github.com/postgres/postgres.git 
cd postgres
git checkout -b REL9_5_STABLE origin/REL9_5_STABLE
./configure --prefix-$HOME/osnapdev/installed    
make 
make install
# use curl to download Apache httpd-2.4.25
cd $HOME
curl http://www.gtlib.gatech.edu/pub/apche//httpd/httpd-2.4.25.tar.bz2
# configure/make/install httpd
tar
