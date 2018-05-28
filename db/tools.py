import pymysql
import json

def get_config(file_name="config"):
    """Get Configuration"""
    with open(file_name, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config

