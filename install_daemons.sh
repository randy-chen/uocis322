# Randy Chen, CIS 322 Assignment 1.

cd $HOME
git clone https://github.com/postgres/postgres.git 
cd postgres
git checkout -b REL9_5_STABLE origin/REL9_5_STABLE
./configure --prefix=/home/osnapdev/installed    
make 
make install

cd $HOME
curl http://www.gtlib.gatech.edu/pub/apache//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2
cd httpd-2.4.25
./configure --prefix=/home/osnapdev/installed
make
make install
