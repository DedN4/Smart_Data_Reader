import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from city_clusters import city_to_cluster

app = Flask(__name__)

# Caminho para o arquivo de planilha
datafile = "data.csv"

# Verifica se o arquivo da planilha já existe
if not os.path.isfile(datafile):
    # Se não existir, cria um DataFrame vazio e salva em um arquivo CSV
    df = pd.DataFrame()
    df.to_csv(datafile, index=False, header=["Protocolo", "Data do Encaixe", "Cidade", "Cluster", "Período", "Motivo", "Gravidade"])

def save_to_csv(data):
    # Verifique se o arquivo CSV já existe
    if os.path.isfile(datafile):
        # Se o arquivo existir, leia-o
        df = pd.read_csv(datafile, encoding='latin-1')
    else:
        # Se o arquivo não existir, crie um DataFrame vazio
        df = pd.DataFrame()

    cidade = request.form["cidade"]
    cluster = city_to_cluster.get(cidade, "Outro")  # Se a cidade não estiver no dicionário, o cluster será "Outro"

    # Adicione os dados com os cabeçalhos
    data["Cluster"] = cluster  # Adiciona automaticamente o cluster com base na cidade
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)

    # Salve o DataFrame de volta no CSV com cabeçalhos
    df.to_csv(datafile, index=False, encoding='latin-1')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        protocolo = request.form["protocolo"]
        data_encaixe = request.form["data_encaixe"]
        cidade = request.form["cidade"]
        periodo = request.form["periodo"]
        motivo = request.form["motivo"]
        gravidade = request.form["gravidade"]

        data = {
            "Protocolo": [protocolo],
            "Data do Encaixe": [data_encaixe],
            "Cidade": [cidade],
            "Período": [periodo],
            "Motivo": [motivo],
            "Gravidade": [gravidade]
        }

        save_to_csv(data)

    # Lê os dados do CSV para exibir na página
    df = pd.read_csv(datafile, encoding='latin-1')
    data = df.to_dict(orient="records")

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
