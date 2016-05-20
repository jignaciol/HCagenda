#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SQLiteBackend
from cork.backends import SqlAlchemyBackend
from constants import BDP_IP, BDP_DBNAME, BDP_PASSWORD, BDP_USER


def populate_backendPSQL():
    b = SqlAlchemyBackend("postgresql+psycopg2://" + BDP_USER + ":" + BDP_PASSWORD + "@" + BDP_IP + "/" + BDP_DBNAME, initialize=True)
    return b


def populate_backend():
    b = SQLiteBackend("loginDB.db", initialize=False)
    return b

session_opts = {
    "session.cookie_expires": True,
    "session.encrypt_key": "por favor use una llave aleatoria y mantengala en secreto!",
    "session.httponly": True,
    "session.timeout": 3600 * 1,  # 1 hour
    "session.type": "cookie",
    "session.validate_key": True,
}
