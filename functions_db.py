import psycopg2
from flask import Flask, json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data


def conectarBD():
    dataConn = loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],
                            user=dataConn["user"], password=dataConn["password"])
    return conn


def cerrarBD(DBconection):
    DBconection.close()


def guardarCambiosEnBD(curs):
    curs.execute("COMMIT")