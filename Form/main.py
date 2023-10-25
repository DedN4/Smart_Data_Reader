import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar
from form import FormularioApp
from dashboard import Dashboard

datafile = "data.csv"

class MainFormulario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulário")
        self.setGeometry(100, 100, 800, 600)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("Arquivo")

        open_form_action = QAction("Abrir Formulário", self)
        open_form_action.triggered.connect(self.open_form)
        file_menu.addAction(open_form_action)

        open_dashboard_action = QAction("Abrir Dashboard", self)
        open_dashboard_action.triggered.connect(self.open_dashboard)
        file_menu.addAction(open_dashboard_action)

        self.dashboard = Dashboard(datafile)
        self.form_widget = FormularioApp()
        self.form_widget.hide()  # Comece com o formulário oculto
        self.setCentralWidget(self.dashboard)

    def open_form(self):
        self.form_widget.show()
        self.dashboard.hide()
        self.setCentralWidget(self.form_widget)

    def open_dashboard(self):
        self.dashboard.show()
        self.form_widget.hide()
        self.setCentralWidget(self.dashboard)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainFormulario()
    ex.show()
    sys.exit(app.exec_())
