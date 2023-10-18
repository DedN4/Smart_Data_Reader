import sys
import pandas as pd
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QPushButton, QFileDialog, QTextBrowser, QVBoxLayout, QWidget, QDockWidget, QTableWidget,QInputDialog, QTableWidgetItem, QMenuBar, QLabel, QComboBox
from datetime import datetime

class AnalisadorXLSX(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SDR - Smart Data Reader")
        self.setGeometry(100, 100, 800, 600)

        # Crie a barra de menu
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
        analise_action.triggered.connect(self.iniciarAnaliseEspecifica)
        analise_menu.addAction(analise_action)

        # Crie um widget central para organizar a interface
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout em grade para organizar a interface
        layout = QVBoxLayout(central_widget)
        central_widget.setLayout(layout)

        # Área para exibir estatísticas gerais
        self.textBrowser = QTextBrowser(self)
        layout.addWidget(self.textBrowser)

        # DataFrame original
        self.df_original = None

        # Elementos de interface do usuário para seleção
        layout.addWidget(QLabel("Selecione a coluna principal:"))
        self.coluna_principal_combobox = QComboBox(self)
        layout.addWidget(self.coluna_principal_combobox)

        layout.addWidget(QLabel("Selecione as colunas para operações adicionais (opcional):"))
        self.colunas_operacoes_combobox = QComboBox(self)
        layout.addWidget(self.colunas_operacoes_combobox)

        # Botão para iniciar a análise
        self.analise_button = QPushButton("Iniciar Análise", self)
        self.analise_button.clicked.connect(self.iniciarAnalise)
        layout.addWidget(self.analise_button)

        # Crie um dock widget para os logs
        self.dock_logs = QDockWidget("Histórico", self)
        self.logs_widget = QTextBrowser(self)
        self.dock_logs.setWidget(self.logs_widget)
        self.addDockWidget(2, self.dock_logs)

        self.log("Bem-vindo ao LID - Leitor Inteligente de Dados.")
        self.log("Ações do usuário registradas")

        # Crie um dock widget para a visualização de dados
        self.dock_visualizacao = QDockWidget("Visualização de Dados", self)
        self.visualizacao_widget = QTableWidget(self)
        self.dock_visualizacao.setWidget(self.visualizacao_widget)
        self.addDockWidget(1, self.dock_visualizacao)
        self.dock_visualizacao.hide()

        # Crie um submenu "Preferências" em "Arquivo"
        preferencias_submenu = arquivo_menu.addMenu("Preferências")

        # Adicione uma ação para mostrar/ocultar logs
        mostrar_logs_action = QAction("Mostrar/Esconder Logs", self)
        mostrar_logs_action.setCheckable(True)
        mostrar_logs_action.toggled.connect(self.toggleLogs)
        preferencias_submenu.addAction(mostrar_logs_action)

        # Crie o menu "Exibir"
        exibir_menu = menubar.addMenu("Exibir")

        # Adicione a ação para mostrar/ocultar logs
        self.toggle_logs_action = exibir_menu.addAction("Mostrar/Esconder Logs")
        self.toggle_logs_action.setCheckable(True)
        self.toggle_logs_action.toggled.connect(self.toggleLogs)

        # Adicione ação para mostrar/ocultar visualização de dados
        self.toggle_visualizacao_action = exibir_menu.addAction("Mostrar/Esconder Visualização de Dados")
        self.toggle_visualizacao_action.setCheckable(True)
        self.toggle_visualizacao_action.toggled.connect(self.toggleVisualizacao)

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

        # Preencha os elementos de seleção de coluna com as colunas disponíveis
        if self.df_original is not None:
            self.coluna_principal_combobox.addItems(self.df_original.columns)
            self.colunas_operacoes_combobox.addItems(self.df_original.columns)

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

    def iniciarAnaliseEspecifica(self):
        # Abra a caixa de diálogo para selecionar a coluna principal
        coluna, ok = QInputDialog.getItem(self, "Selecionar Coluna de Origem", "Selecione a coluna:",
                                          self.df_original.columns, 0, False)

        if ok:
            self.log(f"Iniciou análise específica com base na coluna: {coluna}")
            self.criarTabelaDinamica(coluna)

    def iniciarAnalise(self):
        coluna_principal = self.coluna_principal_combobox.currentText()
        colunas_operacoes = self.colunas_operacoes_combobox.currentText()

        self.log(f"Iniciou análise com base na coluna principal: {coluna_principal} e coluna(s) de operações: {colunas_operacoes}")
        self.criarTabelaDinamica(coluna_principal, colunas_operacoes)

    def criarTabelaDinamica(self, coluna_principal, colunas_operacoes=None):
        if colunas_operacoes:
            colunas_selecionadas = [coluna_principal] + colunas_operacoes.split(", ")
            # Certifique-se de que as colunas selecionadas sejam únicas
            colunas_selecionadas = list(set(colunas_selecionadas))
        else:
            colunas_selecionadas = [coluna_principal]

        tabela_dinamica = self.df_original.groupby(colunas_selecionadas).size().reset_index(name='Quantidade')

        self.visualizacao_widget.setRowCount(tabela_dinamica.shape[0])
        self.visualizacao_widget.setColumnCount(tabela_dinamica.shape[1])
        self.visualizacao_widget.setHorizontalHeaderLabels(tabela_dinamica.columns)

        for row in range(tabela_dinamica.shape[0]):
            for col in range(tabela_dinamica.shape[1]):
                item = QTableWidgetItem(str(tabela_dinamica.iloc[row, col]))
                self.visualizacao_widget.setItem(row, col, item)


def main():
    app = QApplication(sys.argv)
    ex = AnalisadorXLSX()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
