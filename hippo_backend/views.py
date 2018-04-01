# myapp/views.py
import json


def get_index_html():
    f = open("./instance/menu_database.json", encoding='utf-8')
    res = json.load(f)
    return res
