import psycopg2
from flask import Flask
from flask import jsonify
from flask import request
import json

from flask_cors import CORS

app=Flask(__name__)
cors = CORS(app)
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

def guardarCambiosEnBD(curs):
    curs.execute("COMMIT")



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
        #cursor.callproc('', parametros)
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


@app.route("/cliente/<string:emailCliente>",methods=['POST'])
def post_newClaveCliente(emailCliente):
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        # info_result = request.get_json()
        # todo eliminar este diccionario y habilitar el info_result
        info_result = {
            "clave_nueva": "3123566333",
        }
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()
        # Parametros del procedimiento o funcion
        par = (emailCliente, info_result["clave_nueva"])
        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CAMBIO_CLAVE_USUARIO_PR', par)
        #Commit en BD
        guardarCambiosEnBD()
        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/cliente",methods=['POST'])
def add_cliente():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        #info_result = request.get_json()
        #todo eliminar este diccionario y habilitar el info_result
        info_result = {
            "tipo_id": "CC",
            "num_id" : "1013680174",
            "f_nom" : "Juan",
            "s_nom" : "Camilo",
            "f_apell" : "Cespedes",
            "s_apell" : "Romero",
            "tel" : "3123566333",
            "email" : "juankamilocromero@gmail.com"
        }
        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()
        #Parametros del procedimiento o funcion
        par = (info_result["tipo_id"],info_result["num_id"],info_result["f_nom"],info_result["s_nom"],info_result["f_apell"],info_result["s_apell"],info_result["tel"],info_result["email"])
        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CREAR_CLIENTE_FU', par)


        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/verificarDispo",methods=['GET'])
def get_disponibilidad():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()
        #Parametros del procedimiento o funcion
        par = (info_result["nombre_ciudad_p"],info_result["tipo_vehiculo_p"],info_result["es_cubierto_p"],info_result["fecha_entrada_p"],info_result["hora_entrada_p"],info_result["s_apell"],info_result["tel"],info_result["nombre_entrada_p"],info_result["nombre_sucursal_p"])

        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.VERIFICAR_DISPONIBILIDAD_FU', par)


        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/cliente/vehiculo",methods=['POST'])
def set_vehiculo():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()
        #Parametros del procedimiento o funcion
        par = (info_result["tipo_vehiculo_p"],info_result["placa_p"],info_result["nombre_1_p"],info_result["nombre_2_p"],info_result["apellido_1_p"],info_result["apellido_2_p"],info_result["marca_vehiculo_p"],info_result["color_vehiculo_p"])


        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.VERIFICAR_DISPONIBILIDAD_FU', par)


        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/supAdmin/admin",methods=['POST'])
def set_vehiculo():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()
        #Parametros del procedimiento o funcion
        par = (info_result["tipo_identificacion_p"],info_result["numero_identificacion_p"],info_result["NOMBRE1_EMPLEADO_P"],info_result["NOMBRE2_EMPLEADO_P"],info_result["APELLIDO1_EMPLEADO_P"],info_result["APELLIDO2_CLIENTE_P"],info_result["TELEFONO_EMPLEADO_P"],info_result["CORREO_EMPLEADO_P"])


        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CREAR_ADMIN_FU', par)


        # Recuperar los resultados, si los hay
        results = cursor.fetchall()

        # Cerrar el cursor y la conexión
        cursor.close()
        cerrarBD(DBconn)

        # Devolver los resultados como respuesta en formato JSON
        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/supAdmin/operador",methods=['POST'])
def set_vehiculo():
    try:
        # Obtener los parámetros del cuerpo de la solicitud
        info_result = request.get_json()

        # parametros = request.json.get('parametros')

        # Conectarse a la base de datos PostgreSQL
        DBconn = conectarBD()

        # Crear un cursor
        cursor = DBconn.cursor()
        #Parametros del procedimiento o funcion
        par = (info_result["tipo_identificacion_p"],info_result["numero_identificacion_p"],info_result["NOMBRE1_EMPLEADO_P"],info_result["NOMBRE2_EMPLEADO_P"],info_result["APELLIDO1_EMPLEADO_P"],info_result["APELLIDO2_CLIENTE_P"],info_result["TELEFONO_EMPLEADO_P"],info_result["CORREO_EMPLEADO_P"])


        # Ejecutar el procedimiento almacenado
        cursor.callproc('PARQUEADERO.CREAR_OPERADOR_FU', par)


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
---------------------------
    ENDPOINTS PARQUEADEROS
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
        cursor.callproc('PARQUEADERO.MOSTRAR_SUCURSALES_FU', ())
        #print("SELECT * FROM PARQUEADERO.SUCURSAL")
        #cursor.execute("SELECT * FROM PARQUEADERO.SUCURSAL")

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


@app.route("/cliente/vehiculos/marcas", methods=["GET"])
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


if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["host"]+":" + str(dataConfig["port"]))
    app.run()


