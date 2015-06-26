# coding=utf-8
__author__ = 'alex'
from PyQt4.QtCore import QObject, Qt
from PyQt4.QtGui import QSortFilterProxyModel
from PyQt4.QtSql import QSqlQueryModel

from settings import config


class Users(QObject):
    def __init__(self, parent=None):
        super(Users, self).__init__(parent)
        self.model = QSqlQueryModel()
        self.sortProxyModels = {}
        self.init_model()
        self.init_proxy_models()


    def init_model(self):
        self.model.setQuery(u"SELECT concat_ws(' ', firstname, lastname, patrname) "
                            u"AS FIO, "
                            u"CONCAT_WS(', ', birthdate, TIMESTAMPDIFF(YEAR, birthdate, CURDATE())) "
                            u"AS \"Birth date, age\", "
                            u"(CASE WHEN sex=1 THEN 'М' WHEN sex=2 THEN 'Ж' ELSE 'Неопределен' END)  "
                            u"AS sex , "
                            u"concat_ws(' ', test.ClientPolicy.serial, test.ClientPolicy.number) "
                            u"AS 'Policy serial and number', "
                            u"(SELECT name FROM test.rbDocumentType WHERE id = test.ClientDocument.documentType_id) "
                            u"AS \"Document type\", "
                            u"concat_ws(' ', test.ClientDocument.serial, test.ClientDocument.number) "
                            u"AS \"Document serial and number\""

                            u"FROM test.Client "
                            u"LEFT JOIN test.ClientPolicy ON test.Client.id=test.ClientPolicy.client_id "
                            u"LEFT JOIN test.ClientDocument ON test.Client.id=test.ClientDocument.client_id")


    def init_proxy_model(self, name, column):
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(self.model)
        proxy.setFilterKeyColumn(column)
        proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.model = proxy
        self.sortProxyModels[name] = proxy
        return proxy

    def init_proxy_models(self):
        for (name, settings) in config["filter_fields"].items():
            self.init_proxy_model(name, settings["column"])

    def apply_filer(self, text, filter_name):
        self.sortProxyModels[filter_name].setFilterFixedString(text)







