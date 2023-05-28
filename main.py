import psycopg2
from flask import Flask
from flask import jsonify
from flask import request
import json

from flask_cors import CORS

from functions_db import loadFileConfig
from routes.parking import routes_parking
from routes.users import routes_user

app = Flask(__name__)
cors = CORS(app)

app.register_blueprint(routes_user)
app.register_blueprint(routes_parking)

@app.route("/", methods=['GET'])
def test():
    json = {}
    json["message"] = "Server running ..."
    return jsonify(json)


if __name__ == '__main__':
    dataConfig = loadFileConfig()
    print("Server running : " + "http://" + dataConfig["host"] + ":" + str(dataConfig["port"]))
    app.run()
