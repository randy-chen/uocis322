#! /usr/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./export_data.sh <dbname> <output dir>"
    exit;
fi

mkdir $2
cd $2
python3 ../export.py $1 $2
cd ..
cp -R $2 ../import
