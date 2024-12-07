from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro de doador
@app.route('/cadastro', methods=['GET'])
def inserir_doador_form():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/inserir', methods=['POST'])
def inserir_doador():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    tipo_sanguineo = request.form['tipo_sanguineo']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    
    payload = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'tipo_sanguineo': tipo_sanguineo,
        'data_nascimento': data_nascimento,
        'endereco': endereco
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/doadores/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_doadores'))
    else:
        return "Erro ao inserir doador", 500

# Rota para listar todos os doadores
@app.route('/banco', methods=['GET'])
def listar_doadores():
    response = requests.get(f'{API_BASE_URL}/api/v1/doadores/')
    try:
        doadores = response.json()
    except:
        doadores = []
    return render_template('banco.html', doadores=doadores)

# Rota para exibir o formulário de edição de doador
@app.route('/atualizar/<int:doador_id>', methods=['GET'])
def atualizar_doador_form(doador_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/doadores/")
    doadores = [doador for doador in response.json() if doador['id'] == doador_id]
    if len(doadores) == 0:
        return "Doador não encontrado", 404
    doador = doadores[0]
    return render_template('atualizar.html', doador=doador)

# Rota para enviar os dados do formulário de edição de doador para a API
@app.route('/atualizar/<int:doador_id>', methods=['POST'])
def atualizar_doador(doador_id):
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    tipo_sanguineo = request.form['tipo_sanguineo']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    
    payload = {
        'id': doador_id,
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'tipo_sanguineo': tipo_sanguineo,
        'data_nascimento': data_nascimento,
        'endereco': endereco
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/doadores/{doador_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_doadores'))
    else:
        return "Erro ao atualizar doador", 500

# Rota para exibir o formulário de doação
@app.route('/doar/<int:doador_id>', methods=['GET'])
def doar_doador_form(doador_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/doadores/")
    doadores = [doador for doador in response.json() if doador['id'] == doador_id]
    if len(doadores) == 0:
        return "Doador não encontrado", 404
    doador = doadores[0]
    return render_template('doar.html', doador=doador)

# Rota para doar sangue
@app.route('/doar/<int:doador_id>', methods=['POST'])
def doar_doador(doador_id):
    nome_doador = request.form['nome_doador']
    tipo_sanguineo = request.form['tipo_sanguineo']
    data_doacao = datetime.now().strftime('%m/%d/%Y')

    payload = {
        'nome_doador': nome_doador,
        'tipo_sanguineo': tipo_sanguineo,
        'data_doacao': data_doacao
    }

    response = requests.put(f"{API_BASE_URL}/api/v1/doadores/{doador_id}/doar/", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_doadores'))
    else:
        return "Erro ao doar sangue", 500

# Rota para listar todas as doações
@app.route('/doacoes', methods=['GET'])
def listar_doacoes():
    response = requests.get(f"{API_BASE_URL}/api/v1/doacoes/")
    try:
        doacoes = response.json()
    except:
        doacoes = []
    total_doacoes = 0
    for doacao in doacoes:
        total_doacoes += 1
    return render_template('doacoes.html', doacoes=doacoes, total_doacoes=total_doacoes)

# Rota para excluir um doador
@app.route('/excluir/<int:doador_id>', methods=['POST'])
def excluir_doador(doador_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/doadores/{doador_id}")
    
    if response.status_code == 200:
        return redirect(url_for('listar_doadores'))
    else:
        return "Erro ao excluir doador", 500

# Rota para resetar o database
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/reset-database/")
    
    if response.status_code == 200:
        return render_template('confirmacao.html')
    else:
        return "Erro ao resetar o database", 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')


