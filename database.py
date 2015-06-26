__author__ = 'alex'
from PyQt4 import QtSql

from settings import config


def _get_connection(config):
    if QtSql.QSqlDatabase.contains():
        return QtSql.QSqlDatabase.database()
    db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName(config["database_settings"]["host"])
    db.setDatabaseName(config["database_settings"]["name"])
    db.setUserName(config["database_settings"]["username"])
    db.setPassword(config["database_settings"]["password"])
    return db


def make_connection():
    db = _get_connection(config)

    if not db.isOpen():
        if not db.open():
            error = db.lastError().text()
            raise Exception(error)

