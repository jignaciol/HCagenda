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

# En caso de recibir un json a traves de post :: utilizar request.json :P

# ruta de acceso para archivos estaticos

# herramientas


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
                       epx.id_extension, epx.mostrar,
                       ext.numero as telefono, ext.serial,
                       d.descripcion as departamento,
                       dcc.descripcion as correo,
                       dcm.descripcion as celular,
                       dct.descripcion as habitacion
                FROM "Agenda".empleado e
                LEFT JOIN "Agenda"."empleadoExtension" epx ON epx.id_empleado = e.id
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

@bottle.route("api/empleado/:id", method="GET")
def listar_empleado_id(id=0):
    """ funcion que lista un empleados dentro de la base de datos de contactos segun el id indicado """

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """
                SELECT e.ficha, e.cedula, e.nombre, e.apellido,
                       epx.id_extension, epx.mostrar,
                       ext.numero as telefono, ext.serial,
                       d.descripcion as departamento,
                       dcc.descripcion as correo,
                       dcm.descripcion as celular,
                       dct.descripcion as habitacion
                FROM "Agenda".empleado e
                LEFT JOIN "Agenda"."empleadoExtension" epx ON epx.id_empleado = e.id
                LEFT JOIN "Agenda"."Extension" ext ON ext.id = epx.id_extension
                LEFT JOIN "Agenda"."departamento" d ON d.id = e.id_departamento
                LEFT JOIN "Agenda"."datosContacto" dcc ON dcc.id_empleado = e.id and dcc.id_tipo_contacto = 2
                LEFT JOIN "Agenda"."datosContacto" dcm ON dcm.id_empleado = e.id and dcm.id_tipo_contacto = 3
                LEFT JOIN "Agenda"."datosContacto" dct ON dct.id_empleado = e.id and dct.id_tipo_contacto = 4
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


@bottle.route("api/empleado/", method="POST")
def agregar_empleado():
    """ funcion para agregar un empleado a la base de datos """
    pass


@bottle.route("api/empleado/:id", method="PUT")
def actualizar_empleado(id=0):
    """ funcion para actualizar los datos de un empleado en la base de datos """
    pass


@bottle.route("api/empleado/:id", method="DELETE")
def borrar_empleado(id=0):
    """ funcion para borrar un empleado en la base de datos """
    pass

# CODIGO PARA MODELO AREA #


@bottle.route("/api/area", method="GET")
def listar_areas():
    """ funcion para listar todas las areas """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT a.id, a.descripcion, to_char(a.fec_ing, 'DD-MM-YYYY') as fec_ing, a.bl, a.id_tipo_area,
                  ta.descripcion as tipo_area
                  FROM "Agenda"."Area" a
                  LEFT JOIN "Agenda".tipoarea ta ON ta.id = a.id_tipo_area
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

        sql = """ SELECT a.id, a.descripcion, to_char(a.fec_ing, 'DD-MM-YYYY') as fec_ing, a.bl, a.id_tipo_area,
                  ta.descripcion as tipo_area
                  FROM "Agenda"."Area" a
                  LEFT JOIN "Agenda".tipoarea ta ON ta.id = a.id_tipo_area
                  ORDER BY a.id ASC; """

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
    numero = data["numero"]
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    bl = data["bl"]
    csp = data["csp"]
    tipo = data["tipo"]
    modelo = data["modelo"]
    serial = data["serial"]
    mac_pos = data["mac_pos"]
    grupo_captura = data["grupo_captura"]
    status = data["status"]
    lim = data["lim"]
    fecha_inventario = data["fecha_inventario"]

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
    numero = data["numero"]
    fec_ing = data["fec_ing"]
    bl = data["bl"]
    csp = data["csp"]
    tipo = data["tipo"]
    modelo = data["modelo"]
    serial = data["serial"]
    mac_pos = data["mac_pos"]
    grupo_captura = data["grupo_captura"]
    status = data["status"]
    lim = data["lim"]
    fecha_inventario = data["fecha_inventario"]
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


@bottle.route("/api/extension", method="DELETE")
def borrar_extension(id=0):
    """ funcion para borrar una extension en la base de datos """
    pass

# CODIGO PARA MODELO DATOS DE CONTACTO #


@bottle.route("/api/datoscontacto", method="GET")
def listar_datosContacto():
    """ funcion para listar todas los registros de los datos de contacto """
    pass


@bottle.route("/api/datoscontacto", method="GET")
def listar_datoscontacto_id(id):
    """ funcion para listar datoscontacto segun el id enviado """
    pass


@bottle.route("api/extension/", method="POST")
def agregar_datoscontacto():
    """ funcion para agregar una extension a la base de datos """
    pass


@bottle.route("api/extension/:id", method="PUT")
def actualizar_datoscontacto(id=0):
    """ funcion para actualizar los datos de una extension en la base de datos """
    pass


@bottle.route("api/extension/:id", method="DELETE")
def borrar_datoscontacto(id=0):
    """ funcion para borrar una extension en la base de datos """
    pass

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


@bottle.route("api/empleadoextension/", method="GET")
def listar_empleadoextension():
    """ listar todos: empleadoextension """
    pass


@bottle.route("api/empleadoextension/:id", method="GET")
def listar_empleadoextension_id(id):
    """ listar id:  empleadoextension """
    pass


@bottle.route("api/empleadoextension/", method="POST")
def agregar_empleadoextension():
    """ agregar: empleadoextension """
    pass


@bottle.route("api/empleandoextension/:id", method="PUT")
def actualizar_empleadoextension(id=0):
    """ actualizar: empleadoextension """
    pass


@bottle.route("api/empleadoextension/:id", method="DELETE")
def borrar_empleadoextension(id=0):
    """ borrar: empleadoextension """
    pass

# MODELO: tipoarea #


@bottle.route("/api/tipo_area", method="GET")
def listar_tipoarea():
    """ listar todos: tipoarea """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT id, descripcion, to_char(fec_ing, 'DD-MM-YYYY') as fec_ing, bl FROM "Agenda".tipoarea ORDER BY id ASC; """
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

        sql = """ SELECT id, descripcion, to_char(fec_ing, 'DD-MM-YYYY') as fec_ing, bl
                  FROM "Agenda".tipoarea
                  WHERE id = {0}
                  ORDER BY id; """.format(id)
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


@bottle.route("/api/tipo_area", method="PUT")
def actualizar_tipoarea():
    """ actualizar: tipoarea """
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

        sql = """ SELECT id, descripcion, to_char(fec_ing, 'DD-MM-YYYY') as fec_ing, bl FROM "Agenda"."tipoDatoContacto" ORDER BY id ASC; """
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

        sql = """ SELECT id, descripcion, to_char(fec_ing, 'DD-MM-YYYY') as fec_ing, bl
                  FROM "Agenda"."tipoDatoContacto"
                  WHERE id = {0}
                  ORDER BY id; """.format(id)
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
