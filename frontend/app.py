from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro de doador
@app.route('/cadastro/doador', methods=['GET'])
def cadastro_doador_form():
    return render_template('cadastro_doador.html')

# Rota para cadastrar um novo doador
@app.route('/cadastro/doador', methods=['POST'])
def cadastrar_doador():
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
        return redirect(url_for('listar_doador'))
    else:
        return "Erro ao cadastrar doador", 500

# Rota para listar os doadores
@app.route('/doadores', methods=['GET'])
def listar_doadores():
    response = requests.get(f'{API_BASE_URL}/api/v1/doadores/')
    try:
        doadores = response.json()
    except:
        doadores = []
    return render_template('listar_doadores.html', doadores=doadores)

# Rota para editar dados do doador
@app.route('/atualizar/doador/<int:doador_id>', methods=['GET'])
def atualizar_doador_form(doador_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/doadores/{doador_id}")
    if response.status_code != 200:
        return "Doador não encontrado", 404
    doador = response.json()
    return render_template('atualizar_doador.html', doador=doador)

# Rota para atualizar os dados do doador
@app.route('/atualizar/doador/<int:doador_id>', methods=['POST'])
def atualizar_doador(doador_id):
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

    response = requests.patch(f"{API_BASE_URL}/api/v1/doadores/{doador_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_doadores'))
    else:
        return "Erro ao atualizar doador", 500

# Rota para excluir um doador
@app.route('/excluir/doador/<int:doador_id>', methods=['POST'])
def excluir_doador(doador_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/doadores/{doador_id}")
    
    if response.status_code == 200:
        return redirect(url_for('listar_doadores'))
    else:
        return "Erro ao excluir doador", 500

# Rota para exibir o formulário de cadastro de receptor
@app.route('/cadastro/receptor', methods=['GET'])
def cadastro_receptor_form():
    return render_template('cadastro_receptor.html')

# Rota para cadastrar um novo receptor
@app.route('/cadastro/receptor', methods=['POST'])
def cadastrar_receptor():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    tipo_sanguineo = request.form['tipo_sanguineo']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    necessidade_sangue = request.form['necessidade_sangue']
    
    payload = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'tipo_sanguineo': tipo_sanguineo,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
        'necessidade_sangue': necessidade_sangue
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/receptores/', json=payload)
    
    if response.status_code == 201:
        return redirect(url_for('listar_receptor'))
    else:
        return "Erro ao cadastrar receptor", 500

# Rota para listar os receptores
@app.route('/receptores', methods=['GET'])
def listar_receptores():
    response = requests.get(f'{API_BASE_URL}/api/v1/receptores/')
    try:
        receptores = response.json()
    except:
        receptores = []
    return render_template('listar_receptores.html', receptores=receptores)

# Rota para editar dados do receptor
@app.route('/atualizar/receptor/<int:receptor_id>', methods=['GET'])
def atualizar_receptor_form(receptor_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/receptores/{receptor_id}")
    if response.status_code != 200:
        return "Receptor não encontrado", 404
    receptor = response.json()
    return render_template('atualizar_receptor.html', receptor=receptor)

# Rota para atualizar os dados do receptor
@app.route('/atualizar/receptor/<int:receptor_id>', methods=['POST'])
def atualizar_receptor(receptor_id):
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    tipo_sanguineo = request.form['tipo_sanguineo']
    data_nascimento = request.form['data_nascimento']
    endereco = request.form['endereco']
    necessidade_sangue = request.form['necessidade_sangue']
    
    payload = {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'tipo_sanguineo': tipo_sanguineo,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
        'necessidade_sangue': necessidade_sangue
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/receptores/{receptor_id}", json=payload)
    
    if response.status_code == 200:
        return redirect(url_for('listar_receptores'))
    else:
        return "Erro ao atualizar receptor", 500

# Rota para excluir um receptor
@app.route('/excluir/receptor/<int:receptor_id>', methods=['POST'])
def excluir_receptor(receptor_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/receptores/{receptor_id}")
    
    if response.status_code == 200:
        return redirect(url_for('listar_receptores'))
    else:
        return "Erro ao excluir receptor", 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')

