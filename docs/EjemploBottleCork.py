import MySQLdb
import urllib
import urllib2
import requests
import datetime
from ConfigParser import SafeConfigParser

# ***********Pagina temporal para envio de mensajes de texto*********** #
import bottle
from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SQLiteBackend
import logging

# configuracion de base de datos #
cfg = SafeConfigParser()
cfg.read('/opt/hcosticketweb/configuracion/hcosticketweb.cfg')
# cfg.read('hcosticketweb.cfg')

ip = cfg.get('BASE DE DATOS', 'ip')
port = cfg.getint('BASE DE DATOS', 'port')
dbname = cfg.get('BASE DE DATOS', 'dbname')
user = cfg.get('BASE DE DATOS', 'user')
password = cfg.get('BASE DE DATOS', 'password')

# configuracion de servidor #
server_ip = cfg.get('SERVIDOR', 'ip')
server_port = cfg.getint('SERVIDOR', 'port')


class mySql:

    """ Clase de conexion mysql """

    def __init__(self):
        pass

    def conectar(self):
        # Establecemos la conexion con la base de datos

        self.bd = MySQLdb.connect(ip, user, password, dbname, port)

        # Preparamos el cursor que nos va a ayudar a realizar las operaciones con la base de datos
        self.cursor = self.bd.cursor()

    def consultar(self, strSql):
        ''' Cadena SQL a ejecutar '''
        # Ejecutamos un query SQL usando el metodo execute() que nos proporciona el cursor

        cadSQL = strSql
        self.cursor.execute(cadSQL)

        # Extraemos una sola fila usando el metodo fetchone()
        data = self.cursor.fetchall()
        self.bd.close()

        return data


def ordenesAbiertas():
    '''Metodo que permite consultar la Ordenes de
    Servicios Abiertas por los usuarios'''

    rs = False
    cadSQL = """
		select s.firstname, s.lastname,s.mobile,t.number as Ods, 
 			e.name as equipo, 
			dept_name as Dpto, 
			u.name as usuario, 
 			li.value as edificio, 
			t.* 
		from sistemas.ost_ticket t 
		    left join sistemas.ost_staff s on t.staff_id = s.staff_id 
 		    left join sistemas.ost_team e on t.team_id = e.team_id 
 		    left join sistemas.ost_department d on t.dept_id = d.dept_id 
		    left join sistemas.ost_ticket__cdata cd on cd.ticket_id = t.ticket_id 
		    left join sistemas.ost_list_items li on li.id = cd.dsolicitante and li.list_id = 2 
		    left join sistemas.ost_user u on t.user_id = u.id 
		where t.status_id = 1   
	"""

    cnxMySql = mySql()
    cnxMySql.conectar()
    data = cnxMySql.consultar(cadSQL)

    listaTelefonos = []

    for fila in data:
        if fila[2]:
            # print(fila)
            # print(fila[0], fila[1], fila[2], fila[3])
            listaTelefonos.append((fila[2], fila[3], fila[6], fila[7], fila[8], fila[9]))

    for f in listaTelefonos:
        numTelf, numOds, nomUsuario, edificio, piso, departamento = f
	firma = 'BOT_OSTICKET:'
        msjEnviar = firma + " ODS #{0}, usuario:{1}, Area: {2}. fecha:{3}".format(numOds, nomUsuario, edificio, str(datetime.datetime.now()))
        enviarWebService(numTelf, msjEnviar)
	# Envia copia a coordinadora
        enviarWebService('04166661992', msjEnviar)
        rs = True

    return rs


def ordenesAbiertas_usuario(staff_id):
    '''Metodo que permite consultar la Ordenes de
    Servicios Abiertas por los usuarios'''

    rs = False
    cadSQL = '''
            select s.firstname, s.lastname,s.mobile,t.number as Ods,
            e.name as equipo,
            dept_name as Dpto,
            u.name as usuario,
            li.value as edificio,
            t.*
            from sistemas.ost_ticket t
            left join sistemas.ost_staff s on t.staff_id = s.staff_id
            left join sistemas.ost_team e on t.team_id = e.team_id
            left join sistemas.ost_department d on t.dept_id = d.dept_id
            left join sistemas.ost_ticket__cdata cd on cd.ticket_id = t.ticket_id
            left join sistemas.ost_list_items li on li.id = cd.dsolicitante and li.list_id = 2
            left join sistemas.ost_user u on t.user_id = u.id
            where t.status_id = 1 and t.staff_id = {0}
            '''.format(staff_id)

    cnxMySql = mySql()
    cnxMySql.conectar()
    data = cnxMySql.consultar(cadSQL)

    listaTelefonos = []

    for fila in data:
        if fila[2]:
            listaTelefonos.append((fila[2], fila[3], fila[6], fila[7], fila[8], fila[9]))

    for f in listaTelefonos:
        numTelf, numOds, nomUsuario, edificio, piso, departamento = f
	firma = "BOT_OSTICKET:"
        msjEnviar = firma + " ODS #{0}, usuario:{1}, Area: {2}, fecha:{3}".format(numOds, nomUsuario, edificio, str(datetime.datetime.now()))
        enviarWebService(numTelf, msjEnviar)
        rs = True

    return rs


def listar_contactos():
    """ Funcion para listar todos los usuarios miembros de equipos del OSTicket """

    cadSQL = """
                 SELECT stf.firstname,
                       stf.lastname,
                       stf.email,
                       stf.phone,
                       stf.phone_ext,
                       stf.mobile,
                       otm.team_id,
                       stf.*
                FROM sistemas.ost_staff stf, ost_team_member otm
                WHERE   otm.staff_id = stf.staff_id ;
            """

    cnxMySql = mySql()
    cnxMySql.conectar()
    data = cnxMySql.consultar(cadSQL)

    contactos = []

    for fila in data:
        if fila[2]:
            nombre = fila[0].decode('ISO-8859-1').encode('utf-8')
            apellido = fila[1].decode('ISO-8859-1').encode('utf-8')
            contactos.append((nombre, apellido, fila[2], fila[5], fila[7], fila[5] + ',' + str(fila[7])))

    # Retorno la lista de contactos
    return contactos



def enviarWebService(numero, mensaje):
    ''' parametros 2, (string:NumeroTelefono, string:MensajeSMS)

    Metodo que permite enviar via web service a pyLoroWeb un SMS
    a cualquier telefono movil
    '''
    # print(numero, mensaje)
    url = 'http://10.121.0.110:9091/mensaje'
    data = {'var1': mensaje, 'var2': numero}
    # data = urllib.urlencode({'numero': numero, 'mensaje': mensaje})
    # req = urllib2.Request(url, data)
    # response = urllib2.urlopen(req)
    # respuesta = response.read()

    respuesta = requests.post(url, data)
    # print(respuesta)
    # print(type(respuesta))
    # print(response.read())
    return respuesta



# ----SERVIDOR WEB------- #

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
bottle.debug(True)

def populate_backend():
    b = SQLiteBackend('loginDB.db', initialize=False)
    return b

b = populate_backend()
aaa = Cork(backend=b, email_sender='sistemas.hospitalcoromoto@gmail.com', smtp_url='smtp://smtp.gmail.com')

app = bottle.app()
session_opts = {
    'session.cookie_expires': True,
    'session.encrypt_key': 'please use a random key and keep it secret!',
    'session.httponly': True,
    'session.timeout': 3600 * 1,  # 1 hour
    'session.type': 'cookie',
    'session.validate_key': True,
}

app = SessionMiddleware(app, session_opts)



@bottle.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static/')


def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

@bottle.get('/newuser')
def create_user():
    try:
         aaa.create_user('luengoji', 'admin', 'Ign2205!')
         return dict(ok=True, msg='')
    except Exception, e:
         return dict(ok=False, msg=e.message)
 
 
@bottle.get('/')
def login_form():
    """Formulario de autenticacion"""
    return bottle.template('login.html')
 
 
@bottle.post('/')
def login():
    """Authenticate users"""
    username = post_get('username')

    password = post_get('password')
    aaa.login(username, password, success_redirect='/osticket/sms', fail_redirect='/')


@bottle.route('/logout')
def logout():
    aaa.logout(success_redirect='/')
 

@bottle.route('/osticket/sms')
def index():
    """Only authenticated users can see this"""
    aaa.require(fail_redirect='/')
    # Funcion que muestra la pagina con botones de accion
    contactos = listar_contactos()
    output = bottle.template('index.html', listoptions=contactos)
    return output

@bottle.route('/OSTicket/SMS/enviar', method='POST')
def enviar_mensajes():
    # Funcion que envia los mensajes
    aaa.require(fail_redirect='/')
    print "***ENVIANDO MENSAJES MASIVOS DE TICKETS ABIERTOS***"
    func = ordenesAbiertas()
    print "***FINALIZADO***"
    return func


@bottle.route('/OSTicket/SMS/personal', method='POST')
def sms_personal():
    
    aaa.require(fail_redirect='/')
    rs = True
    # Funcion que envia los mensajes
    print "***ENVIANDO MENSAJE PERSONAL***"
    datos = bottle.request.forms.get('datos').split(',')
    mensaje = bottle.request.forms.get('mensaje')
    mobile = datos[0]
    staff_id = datos[1]
    ordenesAbiertas_usuario(staff_id)
    rsms = enviarWebService(mobile, mensaje)

    print "***********Enviando mensaje************"
    print mobile, " -- ", staff_id, " -- ", mensaje
    print "Respuesta pyloro: "
    print rsms
    print "***FINALIZADO***"

    # rs = False

    return rs
 
def main():
    # Start the Bottle webapp
    bottle.run(app=app, quiet=False, reloader=False, host=server_ip, port=server_port)
 
if __name__ == "__main__":
    main()









