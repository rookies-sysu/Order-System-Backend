#!/bin/bash

while ! nc -z db 3306; do sleep 3; done

echo "Web can connect db! Insert data!"

python init_db.py

echo "Insert finished, start the backend!"

python app.py