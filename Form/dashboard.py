import csv
from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class Dashboard(QWidget):
    def __init__(self, datafile):
        super().__init__()

        self.datafile = datafile

        self.initUI()

    def initUI(self):
        menubar = QMenuBar()
        file_menu = menubar.addMenu("Arquivo")
        open_action = QAction("Abrir Histórico", self)
        open_action.triggered.connect(self.open_history)
        file_menu.addAction(open_action)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)  # Defina o número de colunas necessárias
        self.table_widget.setHorizontalHeaderLabels(["Protocolo", "Data do Encaixe", "Cidade", "Cluster", "Período", "Motivo", "Gravidade"])

        layout = QVBoxLayout()
        layout.addWidget(menubar)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

    def open_history(self):
        try:
            with open(self.datafile, 'r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)

            self.table_widget.setRowCount(len(data))
            for row_num, row_data in enumerate(data):
                for col_num, cell_value in enumerate(row_data):
                    item = QTableWidgetItem(cell_value)
                    self.table_widget.setItem(row_num, col_num, item)

        except Exception as e:
            print(f"Erro ao abrir o histórico: {str(e)}")
