import pymysql
import json
from tools import *

path_to_config = "./config"
path_to_sql = "./TinyHippo.sql"

# load config of database
config = get_config(path_to_config)

# connect to dataset
db = pymysql.connect(host=config['localhost']['host'],
                     user=config['localhost']['user'],
                     port=config['localhost']['port'],
                     password=config['localhost']['password'],
                     database=config['localhost']['database'],
                     charset=config['localhost']['charset'])
# create a cursor
cursor = db.cursor()

# create dataset and tables
with open(path_to_sql) as f:
    sql_list = f.read().split(';')[:-1]
    for sql in sql_list:
        cursor.execute(sql + ';')
db.commit()

# close the connection
db.close()
