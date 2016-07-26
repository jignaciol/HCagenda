#!/user/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jignaciol'

import bottle
import psycopg2
import json
import datetime
import cork_server
from constants import BDP_IP, BDP_PORT, BDP_DBNAME, BDP_USER, BDP_PASSWORD
from constants import BTL_HOST, BTL_PORT

DSN = "host='{0}' port={1} dbname='{2}' user='{3}' password='{4}'"
DSN = DSN.format(BDP_IP, BDP_PORT, BDP_DBNAME, BDP_USER, BDP_PASSWORD)

SERVER = bottle.app()

b = cork_server.populate_backendPSQL()
corkServer = cork_server.Cork(backend=b, email_sender="", smtp_url="")

SERVER = cork_server.SessionMiddleware(SERVER, cork_server.session_opts)


def post_get(name):
    """Funcion que devuelve el valor de una variable enviada por POST """
    return bottle.request.forms.get(name)


def json_get(name):
    """Funcion para capturar valores enviados por json"""
    data = bottle.request.json
    return data[name]


def json_result():
    return bottle.request.json

# @bottle.error(404)
# @bottle.error(400)
# def error500(error):
#    return bottle.static_file("contacts/template/error.html", root="public/")


@bottle.route("/fotos/<filename:path>")
def static_images(filename):
    """ Funcion que busca las imagenes de los empleados """
    response = {"OK": False, "msg": ""}
    try:
        img = bottle.static_file(filename, root="../Fotos")
        return img
    except Exception:
        return response


@bottle.route("/api/template/<filename:path>")
def static_template(filename):
    """ Funcion que busca y devuelve el archivo template solicitado """
    return bottle.static_file(filename, root="public/template/")


@bottle.route("/public/<filename:path>")
def static(filename):
    """ Funcion que devuelve los archivos estaticos """
    return bottle.static_file(filename, root="public/")


# punto de inicio de la app #
@bottle.route("/", method="GET")
def index():
    """ Funcion que devuelve solo el index del directorio """
    return bottle.static_file("index.html", root="public/")


# consulta de lista de contactos #

@bottle.route("/extensions/", method="GET")
def listar_extensions():
    """ Funcion que se encarga de listar todas las extensiones existentes
        con el departamento al que pertenecen """
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT  ext.id, ext.numero, ext.modelo,
                        ext.id_departamento, d.descripcion
                FROM "Agenda"."extension" ext
                LEFT JOIN "Agenda".departamento d ON d.id = ext.id_departamento
              """

        cur.execute(sql)
        records = cur.fetchall()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    cur.close()
    return json_result


# consulta de lista de empleados con su extension asignada #

@bottle.route("/empleado/", method="GET")
def listar_empleados():
    """ funcion que lista todos los empleados dentro de la base de datos
        de contactos """

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT e.ficha, e.cedula, e.nombre, e.apellido,
                       epx.id_extension, bl.id as bl, bl.descripcion as estado,
                       ext.numero as telefono, ext.serial,
                       d.id as id_departamento, d.descripcion as departamento,
                       dcc.descripcion as correo,
                       dcm.descripcion as celular,
                       dct.descripcion as habitacion
                FROM "Agenda".empleado e
                LEFT JOIN "Agenda"."empleadoExtension" epx ON epx.id_empleado = e.id
                LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = epx.bl
                LEFT JOIN "Agenda"."extension" ext ON ext.id = epx.id_extension
                LEFT JOIN "Agenda"."departamento" d ON d.id = e.id_departamento
                LEFT JOIN "Agenda"."datosContacto" dcc ON dcc.id_empleado = e.id and dcc.id_tipo_contacto = 2
                LEFT JOIN "Agenda"."datosContacto" dcm ON dcm.id_empleado = e.id and dcm.id_tipo_contacto = 3
                LEFT JOIN "Agenda"."datosContacto" dct ON dct.id_empleado = e.id and dct.id_tipo_contacto = 4
                WHERE char_length(ext.numero) > 0
                ORDER BY e.nombre;
              """

        cur.execute(sql)
        records = cur.fetchall()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    cur.close()
    return json_result


# funciones API RESTFULL #

@bottle.route("/api/empleado", method="GET")
def lista_empleados():
    """ Funcion que lista todos los empleados """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT  e.id,
                        e.ficha,
                        e.voe,
                        e.cedula,
                        e.nombre,
                        e.apellido,
                        e.indicador,
                        to_char(e.fecha_nac, 'DD-MM-YYYY') as fecha_nac,
                        to_char(e.fecha_ing, 'DD-MM-YYYY') as fecha_ing,
                        e.id_departamento
                FROM "Agenda".empleado e
                ORDER BY e.nombre;
              """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/empleado/:id", method="GET")
def listar_empleado_id(id=0):
    """ funcion que lista un empleados dentro de la base de datos de contactos segun el id indicado """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT  e.id,
                        e.ficha,
                        e.voe,
                        e.cedula,
                        e.nombre,
                        e.apellido,
                        e.indicador,
                        to_char(e.fecha_nac, 'DD-MM-YYYY') as fecha_nac,
                        to_char(e.fecha_ing, 'DD-MM-YYYY') as fecha_ing,
                        e.id_departamento
                FROM "Agenda".empleado e
                WHERE e.id = {0}
                ORDER BY e.nombre;
              """.format(id)

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/empleado", method="POST")
def agregar_empleado():
    """ funcion para agregar un empleado a la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    ficha = data["ficha"]
    voe = data["voe"]
    cedula = data["cedula"]
    nombre = data["nombre"].encode("utf-8")
    apellido = data["apellido"].encode("utf-8")
    indicador = data["indicador"].encode("utf-8")
    fecha_nac = data["fecha_nac"]
    id_departamento = data["id_departamento"]
    bl = data["bl"]
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda".empleado', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda".empleado(id, ficha, voe, cedula, nombre, apellido, indicador, fecha_nac, fecha_ing, id_departamento, bl)
                     VALUES ( {0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', {9}, {10} );
              """.format(new_id, ficha, voe, cedula, nombre, apellido, indicador, fecha_nac, today, id_departamento, bl)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/empleado/:id", method="PUT")
def actualizar_empleado(id=0):
    """ funcion para actualizar los datos de un empleado en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    ficha = data["data"]
    voe = data["voe"]
    cedula = data["cedula"]
    nombre = data["nombre"]
    apellido = data["apellido"]
    indicador = data["indicador"]
    fecha_nac = data["fecha_nac"]
    id_departamento = data["id_departamento"]
    bl = data["bl"]

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda".empleado
                  SET ficha={0},
                      voe={1},
                      cedula={2},
                      nombre={3},
                      apellido={4},
                      indicador={5},
                      fecha_nac={6},
                      id_departamento={7},
                      bl={8}
                  WHERE id = {9};""".format(ficha, voe, cedula, nombre, apellido, indicador, fecha_nac, id_departamento, bl)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/empleado/:id", method="DELETE")
def borrar_empleado(id=0):
    """ funcion para borrar un empleado en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda"."datosContacto" WHERE id_empleado = {0} """.format(id)
        cur.execute(sql)
        conn.commit()

        sql = """ DELETE FROM "Agenda".empleado WHERE id = {0};""".format(id)
        cur.execute(sql)
        conn.commit()

        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = "error al intentar borrar el registro en la base de datos"
        print "ERROR: no se pudo borrar el registo -->", error

    return response

# CODIGO PARA MODELO NACIONALIDAD #


@bottle.route("/api/nacionalidad", method="GET")
def listar_nacionalidad():
    """ funcion para listar todas las areas """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT id_nacionalidad, descripcion, bl, codigo FROM "Agenda".nacionalidad;
              """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/nacionalidad/:id", method="GET")
def listar_nacionalidad_id(id):
    """ funcion para listar un area segun el id enviado """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT id_nacionalidad, descripcion, bl, codigo
                FROM "Agenda".nacionalidad
                WHERE id_nacionalidad = {0}
              """.format(id)

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/nacionalidad", method="POST")
def agregar_nacionalidad():
    """ funcion para agregar un empleado a la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data['descripcion']
    bl = data['bl']
    codigo = data['codigo']

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda".nacionalidad', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda".nacionalidad(id, descripcion, bl, codigo)
                     VALUES ({0}, '{1}', {2}, '{3}');
              """.format(new_id, descripcion, bl, codigo)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/nacionalidad", method="PUT")
def actualizar_nacionalidad(id=0):
    """ funcion para actualizar los datos de un area en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"]
    bl = data["bl"]
    codigo = data["codigo"]

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda"."Area"
                  SET bl = {0}, descripcion = '{1}', codigo = '{2}'
                  WHERE id = {3};""".format(bl, descripcion, codigo, id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/nacionalidad", method="DELETE")
def borrar_nacionalidad(id=0):
    """ funcion para borrar un empleado en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda".nacionalidad WHERE id = {0};""".format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = "error al intentar borrar el registro en la base de datos"
        print "ERROR: no se pudo borrar el registo -->", error

    return response


# CODIGO PARA MODELO AREA #


@bottle.route("/api/area", method="GET")
def listar_areas():
    """ funcion para listar todas las areas """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT a.id, a.descripcion, to_char(a.fec_ing, 'DD-MM-YYYY') as fec_ing,
                  bl.id as bl, bl.descripcion as estado,
                  a.id_tipo_area,
                  ta.descripcion as tipo_area
                  FROM "Agenda"."Area" a
                  LEFT JOIN "Agenda".tipoarea ta ON ta.id = a.id_tipo_area
                  LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = a.bl
                  ORDER BY a.id ASC; """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/area/:id", method="GET")
def listar_area_id(id):
    """ funcion para listar un area segun el id enviado """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT a.id, a.descripcion, to_char(a.fec_ing, 'DD-MM-YYYY') as fec_ing,
                  bl.id as bl, bl.descripcion as estado,
                  a.id_tipo_area,
                  ta.descripcion as tipo_area
                  FROM "Agenda"."Area" a
                  LEFT JOIN "Agenda".tipoarea ta ON ta.id = a.id_tipo_area
                  LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = a.bl
                  ORDER BY a.id ASC;
              """

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/area", method="POST")
def agregar_area():
    """ funcion para agregar un empleado a la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data['descripcion']
    bl = data['bl']
    id_tipo_area = data['id_tipo_area']
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda"."Area"', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda"."Area"(id, descripcion, fec_ing, bl, id_tipo_area)
                     VALUES ({0}, '{1}', '{2}', {3}, {4});
              """.format(new_id, descripcion, today, bl, id_tipo_area)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/area", method="PUT")
def actualizar_area(id=0):
    """ funcion para actualizar los datos de un area en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"]
    bl = data["bl"]
    id = data["id"]
    id_tipo_area = data["id_tipo_area"]

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda"."Area"
                  SET bl = {0}, descripcion = '{1}', id_tipo_area = {2}
                  WHERE id = {3};""".format(bl, descripcion, id_tipo_area, id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/area", method="DELETE")
def borrar_area(id=0):
    """ funcion para borrar un empleado en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda"."Area" WHERE id = {0};""".format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = "error al intentar borrar el registro en la base de datos"
        print "ERROR: no se pudo borrar el registo -->", error

    return response


# CODIGO PARA MODELO EXTENSION #


@bottle.route("/api/extension", method="GET")
def listar_extensiones():
    """ funcion para listar todas los registros de las extensiones """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT e.id,
                        d.id as id_departamento, d.descripcion as departamento,
                        e.numero, to_char(e.fec_ing, 'DD-MM-YYYY') as fec_ing,
                        bl.id as bl, bl.descripcion as estado,
                        e.csp, e.tipo, e.modelo,
                        e.serial, mac_pos, e.grupo_captura, e.status, e.lim, e.fecha_inventario
                  FROM "Agenda".extension e
                  LEFT JOIN "Agenda".departamento d ON d.id = e.id_departamento
                  LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = e.bl
                  ORDER BY e.id asc;
              """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/extension/:id", method="GET")
def listar_extension_id(id):
    """ funcion para listar una extension segun el id enviado """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT e.id,
                        d.id as id_departamento, d.descripcion as departamento,
                        e.numero, to_char(e.fec_ing, 'DD-MM-YYYY') as fec_ing,
                        bl.id as bl, bl.descripcion as estado,
                        e.csp, e.tipo, e.modelo,
                        e.serial, mac_pos, e.grupo_captura, e.status, e.lim, e.fecha_inventario
                  FROM "Agenda".extension e
                  LEFT JOIN "Agenda".departamento d ON d.id = e.id_departamento
                  LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = e.bl
                  WHERE e.id={0}
                  ORDER BY e.id asc;
              """.format(id)
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/extension", method="POST")
def agregar_extension():
    """ funcion para agregar una extension a la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    id_departamento = data["id_departamento"]
    numero = data["numero"].encode("utf-8")
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    bl = data["bl"]
    csp = data["csp"].encode("utf-8")
    tipo = data["tipo"].encode("utf-8")
    modelo = data["modelo"].encode("utf-8")
    serial = data["serial"].encode("utf-8")
    mac_pos = data["mac_pos"].encode("utf-8")
    grupo_captura = data["grupo_captura"].encode("utf-8")
    status = data["status"].encode("utf-8")
    lim = data["lim"].encode("utf-8")
    fecha_inventario = data["fecha_inventario"].encode("utf-8")

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda".extension', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda".extension(id, id_departamento, numero, fec_ing, bl, csp, tipo, modelo,
                                                 serial, mac_pos, grupo_captura, status, lim, fecha_inventario)
                                         VALUES ({0}, {1}, '{2}', '{3}', {4}, '{5}', '{6}', '{7}', '{8}',
                                                '{9}', '{10}', '{11}', '{12}', '{13}');
              """.format(new_id, id_departamento, numero, today, bl, csp, tipo, modelo,
                         serial, mac_pos, grupo_captura, status, lim, fecha_inventario)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/extension/:id", method="PUT")
def actualizar_extension(id=0):
    """ funcion para actualizar los datos de una extension en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    id_departamento = data["id_departamento"]
    numero = data["numero"].encode("utf-8")
    fec_ing = data["fec_ing"].encode("utf-8")
    bl = data["bl"]
    csp = data["csp"].encode("utf-8")
    tipo = data["tipo"].encode("utf-8")
    modelo = data["modelo"].encode("utf-8")
    serial = data["serial"].encode("utf-8")
    mac_pos = data["mac_pos"].encode("utf-8")
    grupo_captura = data["grupo_captura"].encode("utf-8")
    status = data["status"].encode("utf-8")
    lim = data["lim"].encode("utf-8")
    fecha_inventario = data["fecha_inventario"].encode("utf-8")

    print data
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda".extension
                  SET id_departamento={0},
                      numero='{1}',
                      fec_ing='{2}',
                      bl={3},
                      csp='{4}',
                      tipo='{5}',
                      modelo='{6}',
                      serial='{7}',
                      mac_pos='{8}',
                      grupo_captura='{9}',
                      status='{10}',
                      lim='{11}',
                      fecha_inventario='{12}'
                  WHERE id = {13};
               """.format(id_departamento, numero, fec_ing, bl, csp, tipo, modelo, serial, mac_pos, grupo_captura, status, lim, fecha_inventario, id)
        print sql
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/extension/:id", method="DELETE")
def borrar_extension(id=0):
    """ funcion para borrar una extension en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda".extension WHERE id={0};""".format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = "error al intentar borrar el registro en la base de datos"
        print "ERROR: no se pudo borrar el registo ", error

    return response


# CODIGO PARA MODELO DATOS DE CONTACTO #


@bottle.route("/api/datocontacto", method="GET")
def listar_datosContacto():
    """ funcion para listar todas los registros de los datos de contacto """
    # corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT dc.id,
                    dc.descripcion,
                    to_char(dc.fec_ing, 'DD-MM-YYYY') as fec_ing,
                    dc.id_empleado,
                    tdc.id as id_tipo_contacto,
                    tdc.descripcion as tipocontacto
                FROM "Agenda"."datosContacto" dc
                LEFT JOIN "Agenda"."tipoDatoContacto" tdc ON tdc.id = dc.id_tipo_contacto;
        """

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/datocontacto/:id", method="GET")
def listar_datoscontacto_id(id=0):
    """ funcion para listar datoscontacto segun el id enviado """
    # corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT dc.id,
                    dc.descripcion,
                    to_char(dc.fec_ing, 'DD-MM-YYYY') as fec_ing,
                    dc.id_empleado,
                    tdc.id as id_tipo_contacto,
                    tdc.descripcion as tipocontacto
                FROM "Agenda"."datosContacto" dc
                LEFT JOIN "Agenda"."tipoDatoContacto" tdc ON tdc.id = dc.id_tipo_contacto;
                WHERE dc.id={0}
                ORDER BY dc.id asc;
              """.format(id)

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/datocontacto", method="POST")
def agregar_datoscontacto():
    """ funcion para agregar una extension a la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"]
    id_empleado = data["id_empleado"]
    id_tipo_contacto = data["id_tipo_contacto"]
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda"."datosContacto"', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda"."datosContacto"(id, descripcion, fec_ing, id_empleado, id_tipo_contacto)
                     VALUES ({0}, '{1}', '{2}', {3}, {4});
              """.format(new_id, descripcion, today, id_empleado, id_tipo_contacto)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/datocontacto/:id", method="PUT")
def actualizar_datoscontacto(id=0):
    """ funcion para actualizar los datos de una extension en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"].encode('utf-8')
    id_empleado = data["id_empleado"]
    id_tipo_contacto = data["id_tipo_contacto"]
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                  UPDATE "Agenda"."datosContacto" dc
                  SET  descripcion='{0}',
                       id_empleado={1},
                       id_tipo_contacto={2}
                  WHERE dc.id={3};
               """.format(descripcion, id_empleado, id_tipo_contacto, id)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/datocontacto/:id", method="DELETE")
def borrar_datoscontacto(id=0):
    """ funcion para borrar una extension en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda"."datosContacto" dc WHERE dc.id={0}; """.format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar borrar el registro en la base de datos'
        print 'ERROR: no se pudo borrar el registo ', error

    return response


# motodos REST para modelo borrado_logico #


@bottle.route("/api/borradologico", method="GET")
def listar_opciones():
    """ funcion para listar todas las opciones de borrado logico """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT b.id, b.descripcion
                  FROM "Agenda"."borradoLogico" b
                  ORDER BY b.id ASC; """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/borradologico/:id", method="GET")
def listar_opciones_id(id=0):
    """ funcion para listar una opcion de borrado logico segun el id """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT b.id, b.descripcion
                  FROM "Agenda"."borradoLogico" b
                  WHERE b.id={0}
                  ORDER BY b.id ASC; """.format(id)
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/borradologico", method="POST")
def agregar_opcion():
    """ funcion para agregar una opciond de borrado en la base de datos """
    pass


@bottle.route("/api/borradologico", method="PUT")
def actualizar_opcion(id=0):
    """ funcion para actualizar los datos de una opcion de borrado en la base de datos """
    pass


@bottle.route("/api/borradologico", method="DELETE")
def borrar_opcion(id=0):
    """ funcion para borrar una opcion de borrado logico en la base de datos """
    pass

# metodos REST para modelo departamento #


@bottle.route("/api/departamento", method="GET")
def listar_departamento():
    """ funcion para listar todas los registros de los departamentos """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                 SELECT  d.id, d.descripcion, to_char(d.fec_ing, 'DD-MM-YYYY') as fec_ing,
                        a.id as id_ubicacion, a.descripcion as ubicacion,
                        b.id as id_piso, b.descripcion as piso,
                        bl.id as bl, bl.descripcion as estado
                 FROM "Agenda"."departamento" d
                 LEFT JOIN "Agenda"."Area" a ON a.id=d.id_ubicacion and a.id_tipo_area=1
                 LEFT JOIN "Agenda"."Area" b ON b.id=d.id_piso and b.id_tipo_area=2
                 LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = d.bl
                 ORDER BY d.id asc;
            """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/departamento/:id", method="GET")
def listar_departamento_id(id):
    """ funcion para listar departamento segun el id enviado """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                 SELECT  d.id, d.descripcion, to_char(d.fec_ing, 'DD-MM-YYYY') as fec_ing,
                        a.id as id_ubicacion, a.descripcion as ubicacion,
                        b.id as id_piso, b.descripcion as piso,
                        bl.id as bl, bl.descripcion as estado
                 FROM "Agenda"."departamento" d
                 LEFT JOIN "Agenda"."Area" a ON a.id=d.id_ubicacion and a.id_tipo_area=1
                 LEFT JOIN "Agenda"."Area" b ON b.id=d.id_piso and b.id_tipo_area=2
                 LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = d.bl
                 WHERE d.id = {0}
                 ORDER BY d.id asc;
              """.format(id)
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print "ERROR: no se pudo realizar la conexion: ", error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/departamento", method="POST")
def agregar_departamento():
    """ funcion para agregar un departamento a la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"]
    bl = data["bl"]
    id_ubicacion = data["id_ubicacion"]
    id_piso = data["id_piso"]
    alias = data["alias"]
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda".departamento', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda".departamento(id, descripcion, fec_ing, bl, id_ubicacion, id_piso, alias)
                     VALUES ({0}, '{1}', '{2}', {3}, {4}, {5}, '{6}');
              """.format(new_id, descripcion, today, bl, id_ubicacion, id_piso, alias)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/departamento/:id", method="PUT")
def actualizar_departamento(id=0):
    """ funcion para actualizar los datos de un departamento en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"].encode('utf-8')
    bl = data["bl"]
    id_ubicacion = data["id_ubicacion"]
    id_piso = data["id_piso"]
    alias = data["alias"]
    # id = data["id"]
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda".departamento
                  SET descripcion = '{0}',
                      bl = {1},
                      id_ubicacion = {2},
                      id_piso = {3},
                      alias = '{4}'
                  WHERE id = {5};
               """.format(descripcion, bl, id_ubicacion, id_piso, alias, id)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/departamento/:id", method="DELETE")
def borrar_departamento(id=0):
    """ funcion para borrar un departamento en la base de datos """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda".departamento WHERE id={0};""".format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar borrar el registro en la base de datos'
        print 'ERROR: no se pudo borrar el registo ', error

    return response

# MODELO: empleadoextension #


@bottle.route("/api/empleadoextension", method="GET")
def listar_empleadoextension():
    """ listar todos: empleadoextension """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT 	ee.id,
                    e.id as id_empleado, TRIM(e.nombre) || ' ' || TRIM(e.apellido) as empleado,
                    ext.id as id_extension, ext.numero,
                    to_char(ee.fec_asignacion, 'DD-MM-YYYY') as fec_asignacion,
                    bl.id as bl, bl.descripcion as estado
                FROM "Agenda"."empleadoExtension" ee
                LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id=ee.bl
                LEFT JOIN "Agenda".empleado e ON e.id=ee.id_empleado
                LEFT JOIN "Agenda".extension ext ON ext.id = ee.id_extension
            """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/empleadoextension/:id", method="GET")
def listar_empleadoextension_id(id=0):
    """ listar id:  empleadoextension """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT 	ee.id,
                    e.id as id_empleado, TRIM(e.nombre) || ' ' || TRIM(e.apellido) as empleado,
                    ext.id as id_extension, ext.numero,
                    to_char(ee.fec_asignacion, 'DD-MM-YYYY') as fec_asignacion,
                    bl.id as bl, bl.descripcion as estado
                FROM "Agenda"."empleadoExtension" ee
                LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id=ee.bl
                LEFT JOIN "Agenda".empleado e ON e.id=ee.id_empleado
                LEFT JOIN "Agenda".extension ext ON ext.id = ee.id_extension
                WHERE ee.id={0};
            """.format(id)

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/empleadoextension", method="POST")
def agregar_empleadoextension():
    """ agregar: empleadoextension """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    id_extension = data["id_extension"]
    id_empleado = data["id_empleado"]
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    bl = data["bl"]

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda"."empleadoExtension"', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """
                  INSERT INTO "Agenda"."empleadoExtension"(id, id_empleado, id_extension, fec_asignacion, bl)
                  VALUES ({0}, {1}, {2}, '{3}', {4});
              """.format(new_id, id_empleado, id_extension, today, bl)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/empleadoextension/:id", method="PUT")
def actualizar_empleadoextension(id=0):
    """ actualizar: empleadoextension """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    id_empleado = data["id_empleado"]
    id_extension = data["id_extension"]
    bl = data["bl"]

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda"."empleadoExtension"
                  SET id_empleado={0},
                      id_extension={1},
                      bl={2}
                  WHERE id={3};
               """.format(id_empleado, id_extension, bl, id)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/empleadoextension/:id", method="DELETE")
def borrar_empleadoextension(id=0):
    """ borrar: empleadoextension """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda"."empleadoExtension" WHERE id={0};""".format(id)
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar borrar el registro en la base de datos'
        print 'ERROR: no se pudo borrar el registo ', error

    return response


# MODELO: tipoarea #


@bottle.route("/api/tipo_area", method="GET")
def listar_tipoarea():
    """ listar todos: tipoarea """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT ta.id, ta.descripcion, to_char(ta.fec_ing, 'DD-MM-YYYY') as fec_ing,
                bl.id as bl, bl.descripcion as estado
                FROM "Agenda".tipoarea ta
                LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = ta.bl
                ORDER BY ta.id ASC;
              """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/tipo_area/:id", method="GET")
def listar_tipoarea_id(id):
    """ listar id:  tipoarea """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                   SELECT ta.id, ta.descripcion, to_char(ta.fec_ing, 'DD-MM-YYYY') as fec_ing,
                   bl.id as bl, bl.descripcion as estado
                   FROM "Agenda".tipoarea ta
                   LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = ta.bl
                   WHERE id = {0}
                   ORDER BY ta.id;
              """.format(id)
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route('/api/tipo_area', method='POST')
def agregar_tipoarea():
    """ agregar: tipoarea """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": "", "id": 0}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data['descripcion']
    bl = data['bl']
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda".tipoarea', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda".tipoarea(id, fec_ing, bl, descripcion)
                     VALUES ({0}, '{1}', {2}, '{3}');
              """.format(new_id, today, bl, descripcion)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/tipo_area/:id", method="PUT")
def actualizar_tipoarea(id=0):
    """ actualizar: tipoarea """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"]
    bl = data["bl"]
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda".tipoarea
                  SET bl = {0}, descripcion = '{1}'
                  WHERE id = {2};""".format(bl, descripcion, id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = False
        response["msg"] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/tipo_area", method="DELETE")
def borrar_tipoarea():
    """ borrar: empleadoextension """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda".tipoarea WHERE id = {0};""".format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response["OK"] = True
    except psycopg2.Error as error:
        response["OK"] = 0
        response["msg"] = 'error al intentar borrar el registro en la base de datos'
        print 'ERROR: no se pudo borrar el registo ', error

    return response

# MODELO: tipodatocontacto #


@bottle.route("/api/tipodatocontacto", method="GET")
def listar_tipodatocontacto():
    """ listar todos: tipodatocontacto """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT tc.id, tc.descripcion, to_char(tc.fec_ing, 'DD-MM-YYYY') as fec_ing,
                       bl.id as bl, bl.descripcion as estado
                FROM "Agenda"."tipoDatoContacto" tc
                LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = tc.bl
                ORDER BY tc.id ASC;
              """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/tipodatocontacto/:id", method="GET")
def listar_tipodatocontacto_id(id):
    """ listar id:  tipodatocontacto """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                 SELECT tc.id, tc.descripcion, to_char(tc.fec_ing, 'DD-MM-YYYY') as fec_ing,
                        bl.id as bl, bl.descripcion as estado
                 FROM "Agenda"."tipoDatoContacto" tc
                 LEFT JOIN "Agenda"."borradoLogico" bl ON bl.id = tc.bl
                 WHERE tc.id={0}
                 ORDER BY tc.id ASC;
              """.format(id)
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("/api/tipodatocontacto", method="POST")
def agregar_tipodatocontacto():
    """ agregar: tipodatocontacto """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    # print data
    descripcion = data['descripcion'].encode('utf-8')
    bl = data['bl']
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql_next_val = """ SELECT nextval(pg_get_serial_sequence('"Agenda"."tipoDatoContacto"', 'id')) as new_id; """

        cur.execute(sql_next_val)
        records = cur.fetchall()
        new_id = records[0][0]
        sql = """ INSERT INTO "Agenda"."tipoDatoContacto"(id, descripcion, fec_ing, bl)
                     VALUES ({0}, '{1}', '{2}', {3});
              """.format(new_id, descripcion, today, bl)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
        response['id'] = new_id
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return response


@bottle.route("/api/tipodatocontacto", method="PUT")
def actualizar_tipodatocontacto(id=0):
    """ actualizar: tipodatocontacto """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    try:
        data = json_result()
    except ValueError:
        print "error capturando json"

    descripcion = data["descripcion"]
    bl = data["bl"]
    id = data["id"]
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ UPDATE "Agenda"."tipoDatoContacto"
                  SET bl = {0}, descripcion = '{1}'
                  WHERE id = {2};""".format(bl, descripcion, id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return response


@bottle.route("/api/tipodatocontacto", method="DELETE")
def borrar_tipodatocontacto():
    """ borrar: tipodatocontacto """
    corkServer.require(fail_redirect="/")
    response = {"OK": False, "msg": ""}
    id = json_result()
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda"."tipoDatoContacto" WHERE id = {0};""".format(id)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        response['OK'] = True
    except psycopg2.Error as error:
        response['OK'] = False
        response['msg'] = 'error al intentar borrar el registro en la base de datos'
        print 'ERROR: no se pudo borrar el registo ', error

    return response


# MODELO: usuario #


@bottle.route("api/usuario/", method="GET")
def listar_usuario():
    """ listar todos: usuarios """
    pass


@bottle.route("api/usuario/:id", method="GET")
def listar_usuario_id(id):
    """ listar id:  usuario """
    pass


@bottle.route("api/usuario/", method="POST")
def agregar_usuario():
    """ agregar: usuario """
    pass


@bottle.route("api/usuario/:id", method="PUT")
def actualizar_usuario(id=0):
    """ actualizar: usuario """
    pass


@bottle.route("api/usuario/:id", method="DELETE")
def borrar_usuario(id=0):
    """ borrar: usuario """
    pass


# MODELO: menuOpcion #


@bottle.route("/api/menuopcion/", method="GET")
def listar_menuopcion():
    """ listar todos: opciones de menu """
    # corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT id_opcion, descripcion, url,
                         to_char(fec_asig, 'DD-MM-YYYY') as fec_asig,
                         to_char(fec_desact, 'DD-MM-YYYY') as fec_desct, bl
                  FROM "Agenda"."menuOpcion"; """
        print sql
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("api/menuopcion/:id", method="GET")
def listar_menuopcion_id(id):
    """ listar id:  opcion de menu """
    pass


@bottle.route("api/menuopcion/", method="POST")
def agregar_menuopcion():
    """ agregar: opcion de menu """
    pass


@bottle.route("api/menuopcion/:id", method="PUT")
def actualizar_menuopcion(id=0):
    """ actualizar: actualizar opcion de menu """
    pass


@bottle.route("api/menuopcion/:id", method="DELETE")
def borrar_menuopcion(id=0):
    """ borrar: opcion de menu """
    pass


# funciones para administracion de sesiones #


@bottle.post("/login")
def login():
    """ usuarios registrados """
    response = {"OK": False, "msg": ""}

    username = unicode(post_get("username"), "utf-8")
    password = unicode(post_get("password"), "utf-8")
    if corkServer.login(username, password):
        response["OK"] = True
        response["msg"] = "login exitoso!"
    else:
        response["OK"] = False
        response["msg"] = "error de autenticación"

    return response


@bottle.get("/createuser")
def createuser_get():
    """ Formulario para crear usuario """
    return bottle.static_file("contacts/template/createuser.html", root="public/")


@bottle.post("/createuser")
def createuser():
    try:
        email = unicode(post_get("email"), "utf-8")
        password = unicode(post_get("password"), "utf-8")
        corkServer.login('admin', 'admin')
        corkServer.create_user(email, "admin", password)
        return dict(ok=True, msg='')
    except Exception, e:
        return dict(ok=False, msg=e.message)


@bottle.post("/getUsername")
def check_login():
    user = post_get("username")
    try:
        corkServer.require(user=user)
    except Exception:
        raise bottle.HTTPError(401)
    return corkServer.current_user.username


@bottle.route("/logout")
def logout():
    corkServer.logout(success_redirect="/")


# punto de inicio del servidor #


def main():
    """ funcion principal """
    bottle.debug(True)
    bottle.run(SERVER, host=BTL_HOST, port=BTL_PORT, reloader=True)

if __name__ == "__main__":
    main()
