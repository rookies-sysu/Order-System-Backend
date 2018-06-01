#!/bin/sh
python3 /script/createDB.py
python3 /script/db_insert.py
python3 /script/data_importer.py