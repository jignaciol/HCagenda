#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'jignaciol'
from os import getcwd, environ
from os.path import expanduser, join, isfile
import ConfigParser

dataFolderPath = expanduser('~')
currentPath = getcwd()
myFileConfig = 'HCagenda.cfg'
finalFileConfig = join(currentPath, myFileConfig)
fc = ConfigParser.ConfigParser(allow_no_value=True)


def read_config_file_option(optionName, sectionName, configFile):
    """ Funcion encargada de realizar la lectura de una opcion del archivo de un archivo de
        configuracion """

    # Intenta leer el archivo de configuracion en busca de la opcion dada
    try:
        # utilizo la funcion get para leer el dato
        optionData = configFile.get(sectionName, optionName)

        # verifico si el valor existe
        if optionData:
            return optionData
        else:
            return False
    except ConfigParser.Error, error:
        print 'Error al intentar leer la opcion', error


def read_environ_variable(variableName):
    """ Funcion que lee una variable del entorno de variables """

    # intenta leer la variable
    try:
        variable_data = environ[variableName]
    except Exception:
        variable_data = ''

    return variable_data


# verifico si el archivo existe
if not isfile(finalFileConfig):
    message = 'El archivo de configuracion "{0}" no fue encontrado'.format(finalFileConfig)
    print message
    print finalFileConfig
else:
    # lee el archivo de configuracion
    fc.read(finalFileConfig)

    # intento leer las secciones del archivo de confiddguracion
    try:
        # SECCION: BASE DE DATOS HIS
        seccionBDP = 'SERVIDOR POSTGRES'

        # ip del servidor postgres
        data_BDP_IP = ''
        nameOptionBDP_IP = 'ip'
        data_BDP_IP = read_config_file_option(nameOptionBDP_IP, seccionBDP, fc)

        # puerto del servidor postgres
        data_BDP_PORT = ''
        nameOptionBDP_PORT = 'port'
        data_BDP_PORT = read_config_file_option(nameOptionBDP_PORT, seccionBDP, fc)

        # nombre de la base de datos postgres
        data_BDP_DBNAME = ''
        nameOptionBDP_DBNAME = 'dbname'
        data_BDP_DBNAME = read_config_file_option(nameOptionBDP_DBNAME, seccionBDP, fc)

        # usuario de la base de datos
        data_BDP_USER = ''
        nameOptionBDP_USER = 'user'
        data_BDP_USER = read_config_file_option(nameOptionBDP_USER, seccionBDP, fc)

        # clave para base de datos postgres
        data_BDP_PASSWORD = read_environ_variable('POSTGRES_PASSWORD')

        # SECCION: BOTTLE
        seccionBTL = 'BOTTLE'

        # host para configurar bottle
        data_BTL_HOST = ''
        nameOptionBTL_HOST = 'host'
        data_BTL_HOST = read_config_file_option(nameOptionBTL_HOST, seccionBTL, fc)

        # puerto para configurar bottle
        data_BTL_PORT = ''
        nameOptionBTL_PORT = 'port'
        data_BTL_PORT = read_config_file_option(nameOptionBTL_PORT, seccionBTL, fc)

        # CONSTANTES

        # variables postgresql
        BDP_IP = data_BDP_IP
        BDP_PORT = data_BDP_PORT
        BDP_DBNAME = data_BDP_DBNAME
        BDP_USER = data_BDP_USER
        BDP_PASSWORD = data_BDP_PASSWORD

        # variables bottle
        BTL_HOST = data_BTL_HOST
        BTL_PORT = data_BTL_PORT

    except ConfigParser.Error, error:
        print 'Error al cargar la configuracion: ', error
