#!/bin/bash
set -e

while ! nc -z db 3306; do sleep 3; done

echo "Web can connect db!"

# exec python init_db.py

if [ "$ENV" = "DEV" ]; then
    echo "Running deployment application"
    exec python app.py

elif [ "$ENV" = "TEST" ]; then
    echo "Running test application"
    exec pytest

else
    echo "Please provide an environment"
    echo "Stopping"
fi