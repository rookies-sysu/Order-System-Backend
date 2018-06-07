#!/bin/bash

while ! nc -z db 3306; do sleep 3; done

echo "Web can connect db! Start the web app!"

python app.py