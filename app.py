from flask import Flask
import json
from flask.json import jsonify
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_index_json():
    filename = os.path.join(app.instance_path, 'menu_database.json')
    f = open(filename, encoding='utf-8')
    res = json.load(f)
    return jsonify(res)


# @app.route('/confirm', methods=['POST'])
# def buy():
#     blablabla...

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
