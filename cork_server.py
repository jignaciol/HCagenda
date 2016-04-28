#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beaker.middleware import SessionMiddleware
from cork import Cork
from cork.backends import SQLiteBackend


def populate_backend():
    b = SQLiteBackend("loginDB.db", initialize=False)
    return b

b = populate_backend()
corkServer = Cork(backend=b, email_sender="", smtp_url="")

session_opts = {
    "session.cookie_expires": True,
    "session.encrypt_key": "por favor use una llave aleatoria y mantengala en secreto!",
    "session.httponly": True,
    "session.timeout": 3600 * 1,  # 1 hour
    "session.type": "cookie",
    "session.validate_key": True,
}

corkServer = SessionMiddleware(corkServer, session_opts)
