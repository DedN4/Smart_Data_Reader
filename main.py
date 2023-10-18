import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget, QDockWidget, QToolButton, QMenu, QTableWidget, QTableWidgetItem

class AnalisadorXLSX(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("LID - Leitor Inteligente de Dados")
        self.setGeometry(100, 100, 800, 600)

        # Crie um widget central para organizar a interface
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout em grade para organizar a interface
        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)

        # Botão para importar arquivo XLSX
        self.btnAbrirArquivo = QPushButton("Importar Dados", self)
        self.btnAbrirArquivo.clicked.connect(self.abrirArquivo)
        layout.addWidget(self.btnAbrirArquivo)

        # Área para exibir estatísticas gerais
        self.textBrowser = QTextBrowser(self)
        layout.addWidget(self.textBrowser)

        # DataFrame original
        self.df_original = None

        # Crie um dock widget para os logs
        self.dock_logs = QDockWidget("Histórico", self)
        self.logs_widget = QTextBrowser(self)
        self.dock_logs.setWidget(self.logs_widget)
        self.addDockWidget(2, self.dock_logs)

        # Crie um botão com um menu suspenso para mostrar/ocultar os logs
        self.log_button = QToolButton(self)
        self.log_button.setText("Preferências")
        self.log_button.setPopupMode(QToolButton.MenuButtonPopup)

        # Crie um menu para o botão de logs
        self.log_menu = QMenu(self.log_button)
        self.log_button.setMenu(self.log_menu)

        # Adicione ação para mostrar/ocultar logs
        self.toggle_logs_action = self.log_menu.addAction("Mostrar/Esconder Logs")
        self.toggle_logs_action.setCheckable(True)
        self.toggle_logs_action.toggled.connect(self.toggleLogs)

        layout.addWidget(self.log_button)

        # Crie uma tabela para exibir os dados da planilha
        self.table = QTableWidget(self)
        layout.addWidget(self.table)
        self.table.hide()

    def abrirArquivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo XLSX", "", "Arquivos XLSX (*.xlsx);;Todos os Arquivos (*)", options=options)

        if filepath:
            df = pd.read_excel(filepath)
            self.df_original = df
            self.addLogEntry("Arquivo carregado com sucesso.")
            self.displayDataInTable()

    def addLogEntry(self, entry):
        # Adicione uma entrada ao widget de logs
        self.logs_widget.append(entry)

    def toggleLogs(self):
        # Exibe ou oculta o dock de logs com base na ação do menu
        if self.toggle_logs_action.isChecked():
            self.dock_logs.show()
        else:
            self.dock_logs.hide()

    def displayDataInTable(self):
        # Exiba os dados da planilha na tabela
        if self.df_original is not None:
            self.table.setRowCount(self.df_original.shape[0])
            self.table.setColumnCount(self.df_original.shape[1])
            self.table.setHorizontalHeaderLabels(self.df_original.columns)

            for row in range(self.df_original.shape[0]):
                for col in range(self.df_original.shape[1]):
                    item = QTableWidgetItem(str(self.df_original.iloc[row, col]))
                    self.table.setItem(row, col, item)

            self.table.show()

def main():
    app = QApplication(sys.argv)
    ex = AnalisadorXLSX()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
