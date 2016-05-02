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

# CONSTANTES #
OP_STATUS = {'status': 0, 'message': ''}

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
    return bottle.request.json.get(name)


def json_full():
    """ Funcion que devuelve todo el json enviado por POST """
    return bottle.request.json()


@bottle.error(404)
@bottle.error(400)
def error500(error):
    return bottle.static_file("contacts/template/error.html", root="public/")


@bottle.route("/fotos/<filename:path>")
def static_images(filename):
    """ Funcion que busca las imagenes de los empleados """
    return bottle.static_file(filename, root="../Fotos")


@bottle.route("/public/<filename:path>")
def static(filename):
    """ Funcion que devuelve los archivos estaticos """
    return bottle.static_file(filename, root="public/")


# punto de inicio de la app #
@bottle.route("/", method="GET")
def index():
    """ Funcion que devuelve solo el index del directorio """
    return bottle.static_file("contacts/template/index.html", root="public/")


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
                FROM "Agenda"."Extension" ext
                LEFT JOIN "Agenda".departamento d ON d.id = ext.id_departamento
              """

        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

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
                LEFT JOIN "Agenda"."Extension" ext ON ext.id = epx.id_extension
                LEFT JOIN "Agenda"."departamento" d ON d.id = e.id_departamento
                LEFT JOIN "Agenda"."datosContacto" dcc ON dcc.id_empleado = e.id and dcc.id_tipo_contacto = 2
                LEFT JOIN "Agenda"."datosContacto" dcm ON dcm.id_empleado = e.id and dcm.id_tipo_contacto = 3
                LEFT JOIN "Agenda"."datosContacto" dct ON dct.id_empleado = e.id and dct.id_tipo_contacto = 4
                WHERE char_length(ext.numero) > 0
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


@bottle.route("api/area/", method="GET")
def listar_areas():
    """ funcion para listar todas las areas """
    pass


@bottle.route("api/area/:id", method="GET")
def listar_area_id(id):
    """ funcion para listar un area segun el id enviado """
    pass


@bottle.route("api/area/", method="POST")
def agregar_area():
    """ funcion para agregar un empleado a la base de datos """
    pass


@bottle.route("api/area/:id", method="PUT")
def actualizar_area(id=0):
    """ funcion para actualizar los datos de un area en la base de datos """
    pass


@bottle.route("api/area/:id", method="DELETE")
def borrar_area(id=0):
    """ funcion para borrar un empleado en la base de datos """
    pass

# CODIGO PARA MODELO EXTENSION #


@bottle.route("api/extension/", method="GET")
def listar_extensiones():
    """ funcion para listar todas los registros de las extensiones """
    pass


@bottle.route("api/extension/:id", method="GET")
def listar_extension_id(id):
    """ funcion para listar una extension segun el id enviado """
    pass


@bottle.route("api/extension/", method="POST")
def agregar_extension():
    """ funcion para agregar una extension a la base de datos """
    pass


@bottle.route("api/extension/:id", method="PUT")
def actualizar_extension(id=0):
    """ funcion para actualizar los datos de una extension en la base de datos """
    pass


@bottle.route("api/extension/:id", method="DELETE")
def borrar_extension(id=0):
    """ funcion para borrar una extension en la base de datos """
    pass

# CODIGO PARA MODELO DATOS DE CONTACTO #


@bottle.route("api/datoscontacto/", method="GET")
def listar_datosContacto():
    """ funcion para listar todas los registros de los datos de contacto """
    pass


@bottle.route("api/datoscontacto/:id", method="GET")
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

# metodos REST para modelo departamento #


@bottle.route("api/departamento/", method="GET")
def listar_departamento():
    """ funcion para listar todas los registros de los departamentos """
    pass


@bottle.route("api/departamento/:id", method="GET")
def listar_departamento_id(id):
    """ funcion para listar departamento segun el id enviado """
    pass


@bottle.route("api/departamento/", method="POST")
def agregar_departamento():
    """ funcion para agregar un departamento a la base de datos """
    pass


@bottle.route("api/departamento/:id", method="PUT")
def actualizar_departamento(id=0):
    """ funcion para actualizar los datos de un departamento en la base de datos """
    pass


@bottle.route("api/departamento/:id", method="DELETE")
def borrar_departamento(id=0):
    """ funcion para borrar un departamento en la base de datos """
    pass

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


@bottle.route("api/tipo_area/", method="GET")
def listar_tipoarea():
    """ listar todos: tipoarea """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT id, descripcion, to_char(fec_ing, 'DD-MM-YYYY') as fec_ing, bl FROM "Agenda".tipoarea; """
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("api/tipo_area/:id", method="GET")
def listar_tipoarea_id(id):
    """ listar id:  tipoarea """
    corkServer.require(fail_redirect="/")
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ SELECT id, descripcion, to_char(fec_ing, 'DD-MM-YYYY') as fec_ing, bl
                  FROM "Agenda".tipoarea
                  WHERE id = {0}; """.format(id)
        cur.execute(sql)
        records = cur.fetchall()
        cur.close()
    except psycopg2.Error as error:
        print 'ERROR: no se pudo realizar la conexion: ', error

    cabecera = [col[0] for col in cur.description]
    json_result = json.dumps([dict(zip(cabecera, rec)) for rec in records])

    return json_result


@bottle.route("api/tipo_area/", method="POST")
def agregar_tipoarea():
    """ agregar: tipoarea """

    descripcion = json_get('descripcion')
    bl = json_get('bl')
    today = datetime.datetime.today().strftime('%Y-%m-%d')

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ INSERT INTO "Agenda".tipoarea(fec_ing, bl, descripcion)
                     VALUES ('{0}', {1}, '{2}');
              """.format(today, bl, descripcion)

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        OP_STATUS['status'] = 1
    except psycopg2.Error as error:
        OP_STATUS['status'] = 0
        OP_STATUS['message'] = 'error al insertar el registro a la base de datos'
        print 'ERROR: no se pudo insertar el registo ', error

    return OP_STATUS


@bottle.route("api/tipo_area/:id", method="PUT")
def actualizar_tipoarea(id=0):
    """ actualizar: tipoarea """

    descripcion = json_get("descripcion")
    bl = json_get("bl")

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

        OP_STATUS['status'] = 1
    except psycopg2.Error as error:
        OP_STATUS['status'] = 0
        OP_STATUS['message'] = 'error al intentar actualizar el registro en la base de datos'
        print 'ERROR: no se pudo actualizar el registo ', error

    return OP_STATUS


@bottle.route("api/tipo_area/:id", method="DELETE")
def borrar_tipoarea(id):
    """ borrar: empleadoextension """

    print "borrando"

    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()

        sql = """ DELETE FROM "Agenda".tipoarea WHERE id = {0};""".format(id)
        print sql

        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()

        OP_STATUS['status'] = 1
    except psycopg2.Error as error:
        OP_STATUS['status'] = 0
        OP_STATUS['message'] = 'error al intentar borrar el registro en la base de datos'
        print 'ERROR: no se pudo borrar el registo ', error

    return OP_STATUS

# MODELO: tipodatocontacto #


@bottle.route("api/tipodatocontacto/", method="GET")
def listar_tipodatocontacto():
    """ listar todos: tipodatocontacto """
    pass


@bottle.route("api/tipodatocontacto/:id", method="GET")
def listar_tipodatocontacto_id(id):
    """ listar id:  tipodatocontacto """
    pass


@bottle.route("api/tipodatocontacto/", method="POST")
def agregar_tipodatocontacto():
    """ agregar: tipodatocontacto """
    pass


@bottle.route("api/tipodatocontacto/:id", method="PUT")
def actualizar_tipodatocontacto(id=0):
    """ actualizar: tipodatocontacto """
    pass


@bottle.route("api/tipodatocontacto/:id", method="DELETE")
def borrar_tipodatocontacto(id=0):
    """ borrar: tipodatocontacto """
    pass

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


# funciones para administracion de sesiones #


@bottle.post("/login")
def login():
    """ usuarios registrados """
    email = post_get("email")
    password = post_get("password")
    if corkServer.login(email, password):
        OP_STATUS['status'] = True
        OP_STATUS['message'] = "login exitoso!"
    else:
        OP_STATUS['status'] = False
        OP_STATUS['message'] = "error de autenticación"

    return OP_STATUS


@bottle.route("/logout")
def logout():
    SERVER.logout(success_redirect="/")


# punto de inicio del servidor #


def main():
    """ funcion principal """
    bottle.debug(True)
    bottle.run(SERVER, host=BTL_HOST, port=BTL_PORT, reloader=True)

if __name__ == "__main__":
    main()
