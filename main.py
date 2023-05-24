import psycopg2
from flask import Flask
from flask import jsonify
import json



app=Flask(__name__)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

def conectarBD():
    dataConn = loadFileConfig()
    conn = psycopg2.connect(host=dataConn["host"], port=dataConn["port"], database=dataConn["database"],user=dataConn["user"], password=dataConn["password"])
    return conn
def cerrarBD(DBconection):
    DBconection.close()

def consultaSelect(infoAimprimir,tablas):
    #en infoAimprimir agregar * o la informacion que se desea realizar
    #agregar a tablas tod lo que se escriba despues del from
    return  "SELECT "+infoAimprimir+" FROM PARQUEADERO."+tablas


@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)
"""
---------------------------
    ENDPOINTS USUARIOS
--------------------------
"""
@app.route("/cliente/<string:cliente_id>",methods=['GET'])
def get_clienteByid(cliente_id):
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        # cursor.callproc('nombre_procedimiento', parametros)
        print("SELECT * FROM PARQUEADERO.CLIENTE")
        cursor.execute("SELECT * FROM PARQUEADERO.CLIENTE WHERE K_CLIENTE = "+str(cliente_id))

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


   #todo El de agregar cliente se hace con un callproc de la BD que no esta aun definida.

"""
---------------------------
    ENDPOINTS CLIENTE PARQUEADEROS
--------------------------
"""

@app.route("/cliente/parqueaderos", methods=['GET'])
def get_parqueaderos():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        #parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        #cursor.callproc('nombre_procedimiento', parametros)
        print("SELECT * FROM PARQUEADERO.SUCURSAL")
        cursor.execute("SELECT * FROM PARQUEADERO.SUCURSAL")

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(response)


"""
---------------------------
    ENDPOINTS ClIENTE VEHICULO
--------------------------
"""


@app.route("/cliente/vehiculos/marcas>", methods=["GET"])
def get_marcas():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()

        # Ejecutar el procedimiento almacenado
        # cursor.callproc('nombre_procedimiento', parametros)
        print("SELECT * FROM PARQUEADERO.MARCA_VEHICULO")
        cursor.execute("SELECT * FROM PARQUEADERO.MARCA_VEHICULO")

        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""
@app.route("/cliente/<string:cliente_id>/vehiculo/", methods=['POST'])
def get_result(cliente_id):
    info_result = request.get_json()
    response = ctrVehiculo.create(info_result, cliente_id)
    return jsonify(response)

"""
"""
---------------------------
    ENDPOINTS RESERVAS
--------------------------
"""
"""


@app.route("/cliente/<string:cliente_id>/vehiculo/<string:tipo_vehiculo>", methods=['GET'])
def get_vehiculo_clasificado(cliente_id, tipo_vehiculo):
    response = ctrVehiculo.index(cliente_id, tipo_vehiculo)
    return jsonify(response)


@app.route("/cliente/sucursal/vehiculo/<string:tipo_vehiculo>", methods=['GET'])
def get_vehiculo_clasificado(cliente_id, tipo_vehiculo):
    response = ctrVehiculo.index(cliente_id, tipo_vehiculo)
    return jsonify(response)

@app.route("/cliente/ciudades", methods=['GET'])
def get_ciudades():
    response = ctrCiudad.index()
    return jsonify(response)


@app.route("/cliente/ciudad/<string:ciudad_id>/sucursal/<string:tipo_sucursal>", methods=['GET'])
def get_by_ciudad_tsucursal(ciudad_id, tipo_sucursal):
    response = ctrCiudad.index(ciudad_id, tipo_sucursal)
    return jsonify(response)


@app.route("/cliente/sucursal/<string:id_sucursal>", methods=['GET'])
def get_sucursal(id_sucursal):
    response = ctrCiudad.index(id_sucursal)
    return jsonify(response)


@app.route("/cliente/<string:cliente_id>/sucursal/<string:sucursal_id>/<string:vehiculo_id>", methods=["POST"])
def create_reserva(cliente_id, sucursal_id,vehiculo_id):
    info_result = request.get_json()
    response = ctrSucursal.create(info_result, cliente_id, sucursal_id, vehiculo_id)
    return jsonify(response)


@app.route("/result/<string:result_id>", methods=['PUT'])
def update_result(result_id):
    data = request.get_json()
    response = result_controller.update(result_id, data)
    return jsonify(response)


@app.route("/result/<string:result_id>", methods=['DELETE'])
def delete_result(result_id):
    response = result_controller.delete(result_id)
    return jsonify(response)



"""

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["host"]+":" + str(dataConfig["port"]))
    app.run()


