#!-*-coding:utf-8-*-
import sys
from PyQt4 import uic

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from settings import config
from database import make_connection
from User import Users

( Ui_MainWindow, QMainWindow ) = uic.loadUiType('MainWindow.ui')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mainLayout = QVBoxLayout()
        self.centralWidget().setLayout(self.mainLayout)

        self.find_lines = []

        self.create_connection()


    def create_connection(self):
        try:
            make_connection()
            self.db_connection_success()
        except Exception, exc:
            self.db_connection_error(exc)

    def db_connection_error(self, exc):
        QMessageBox.critical(None,
                             self.tr("Database connection error"),
                             self.tr("Error while connect to database!\nError: ") + exc.message)
        sys.exit(-1)


    def db_connection_success(self):
        self.statusBar().showMessage(self.tr("Database connection established"), 2000)

        self.init_clents_view()
        self.init_search_form()
        self.init_clear_button()

    def create_search_widget(self, form_layout, settings):
        line = QLineEdit()
        self.find_lines.append(line)
        line.connect(line, SIGNAL("textChanged(QString)"), lambda text: self.clients.apply_filer(text, settings[0]))
        form_layout.addRow(settings[1]["label_text"], line)

    def init_search_form(self):
        form_layout = QFormLayout()
        for filter_settings in config["filter_fields"].items():
            self.create_search_widget(form_layout, filter_settings)

        self.mainLayout.addLayout(form_layout)

    def init_clear_button(self):
        button_layout = QHBoxLayout()
        button_layout.addStretch(10)
        button = QPushButton(self.tr("Clear find fields"))
        button.connect(button, SIGNAL("clicked()"), lambda: [line.clear() for line in self.find_lines])
        button_layout.addWidget(button)

        self.mainLayout.addLayout(button_layout)

    def init_clents_view(self):
        self.clients = Users()

        clients_view = QTableView()
        clients_view.setModel(self.clients.model)
        clients_view.resizeColumnsToContents()
        clients_view.horizontalHeader().setStretchLastSection(True)
        clients_view.setSortingEnabled(True)

        self.mainLayout.addWidget(clients_view)

    def __del__(self):
        self.ui = None


# -----------------------------------------------------#
if __name__ == '__main__':
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName('pyqt-test')

    # create widget
    w = MainWindow()
    w.setWindowTitle(w.tr("Clients info"))
    w.showMaximized()

    # connection
    QObject.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))

    # execute application
    sys.exit(app.exec_())