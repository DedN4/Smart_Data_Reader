import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget, QDockWidget, QToolButton, QMenu, QTableWidget, QTableWidgetItem, QAction, QMenuBar
from datetime import datetime

class AnalisadorXLSX(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SDR - Smart Data Reader")
        self.setGeometry(100, 100, 800, 600)

        # Crie um widget central para organizar a interface
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout em grade para organizar a interface
        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)

        # Adicione a barra de menu
        menubar = self.menuBar()

        # Crie o menu "Arquivo"
        arquivo_menu = menubar.addMenu("Arquivo")

        # Opção para importar arquivo XLSX
        importar_action = QAction("Importar Dados", self)
        importar_action.triggered.connect(self.abrirArquivo)
        arquivo_menu.addAction(importar_action)

        # Crie o menu "Análise"
        analise_menu = menubar.addMenu("Análise")

        # Opção para análise específica
        analise_action = QAction("Análise Específica", self)
        analise_action.triggered.connect(self.analiseEspecifica)
        analise_menu.addAction(analise_action)

        # Área para exibir estatísticas gerais
        self.textBrowser = QTextBrowser(self)
        layout.addWidget(self.textBrowser)

        # DataFrame original
        self.df_original = None

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

        # Adicione ação para mostrar/ocultar visualização de dados
        self.toggle_visualizacao_action = self.log_menu.addAction("Mostrar/Esconder Visualização de Dados")
        self.toggle_visualizacao_action.setCheckable(True)
        self.toggle_visualizacao_action.toggled.connect(self.toggleVisualizacao)

        layout.addWidget(self.log_button)

        # Crie um dock widget para os logs
        self.dock_logs = QDockWidget("Histórico", self)
        self.logs_widget = QTextBrowser(self)
        self.dock_logs.setWidget(self.logs_widget)
        self.addDockWidget(2, self.dock_logs)

        self.log("Bem-vindo ao LID - Leitor Inteligente de Dados.")
        self.log("Ações do usuário registradas:")

        # Crie um dock widget para a visualização de dados
        self.dock_visualizacao = QDockWidget("Visualização de Dados", self)
        self.visualizacao_widget = QTableWidget(self)
        self.dock_visualizacao.setWidget(self.visualizacao_widget)
        self.addDockWidget(1, self.dock_visualizacao)
        self.dock_visualizacao.hide()

    def log(self, entry):
        # Registre uma entrada no widget de logs
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {entry}"
        self.logs_widget.append(log_entry)

    def abrirArquivo(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filepath, _ = QFileDialog.getOpenFileName(self, "Abrir Arquivo XLSX", "", "Arquivos XLSX (*.xlsx);;Todos os Arquivos (*)", options=options)

        if filepath:
            self.log(f"Arquivo importado: {filepath}")
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

    def toggleVisualizacao(self):
        # Exibe ou oculta o dock de visualização de dados com base na ação do menu
        if self.toggle_visualizacao_action.isChecked():
            self.dock_visualizacao.show()
        else:
            self.dock_visualizacao.hide()

    def displayDataInTable(self):
        # Exiba os dados da planilha na tabela
        if self.df_original is not None:
            self.visualizacao_widget.setRowCount(self.df_original.shape[0])
            self.visualizacao_widget.setColumnCount(self.df_original.shape[1])
            self.visualizacao_widget.setHorizontalHeaderLabels(self.df_original.columns)

            for row in range(self.df_original.shape[0]):
                for col in range(self.df_original.shape[1]):
                    item = QTableWidgetItem(str(self.df_original.iloc[row, col]))
                    self.visualizacao_widget.setItem(row, col, item)

    def analiseEspecifica(self):
        # Adicione sua lógica para análise específica aqui
        self.textBrowser.clear()
        self.textBrowser.append("Executando análise específica...")

def main():
    app = QApplication(sys.argv)
    ex = AnalisadorXLSX()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
