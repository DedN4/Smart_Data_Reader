import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Caminho para o arquivo de planilha
datafile = "data.csv"

# Verifica se o arquivo da planilha já existe
if not os.path.isfile(datafile):
    # Se não existir, cria um DataFrame vazio e salva em um arquivo CSV
    df = pd.DataFrame(columns=["Protocolo", "Data do Encaixe", "Cidade", "Cluster", "Período", "Motivo", "Gravidade"])
    df.to_csv(datafile, index=False)

def save_to_csv(data):
    # Lê os dados existentes do CSV
    df = pd.read_csv(datafile)
    # Adiciona os novos dados ao DataFrame
    df = df.append(data, ignore_index=True)
    # Salva o DataFrame de volta no CSV
    df.to_csv(datafile, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        protocolo = request.form["protocolo"]
        data_encaixe = request.form["data_encaixe"]
        cidade = request.form["cidade"]
        cluster = request.form["cluster"]
        periodo = request.form["periodo"]
        motivo = request.form["motivo"]
        gravidade = request.form["gravidade"]

        data = {
            "Protocolo": [protocolo],
            "Data do Encaixe": [data_encaixe],
            "Cidade": [cidade],
            "Cluster": [cluster],
            "Período": [periodo],
            "Motivo": [motivo],
            "Gravidade": [gravidade]
        }

        save_to_csv(data)

    # Lê os dados do CSV para exibir na página
    df = pd.read_csv(datafile)
    data = df.to_dict(orient="records")

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
