#! /bin/bash

cd /home/lib/web

python3 app/database/init_db.py

python3 web.py