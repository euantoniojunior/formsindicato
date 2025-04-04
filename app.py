import os
import psycopg2
from psycopg2 import pool
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import pandas as pd

app = Flask(__name__)

# Configurar um pool de conexões
DATABASE_URL = os.getenv("DATABASE_URL")
connection_pool = pool.SimpleConnectionPool(1, 10, dsn=DATABASE_URL, sslmode='disable')

# Obter uma conexão do pool
def get_db_connection():
    return connection_pool.getconn()

# Liberar a conexão de volta para o pool
def release_db_connection(conn):
    connection_pool.putconn(conn)

# Criar tabela se não existir
def criar_tabela():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS cadastros (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    nome_empresa TEXT,
                    telefone TEXT,
                    cidade TEXT,
                    segmento TEXT,
                    curso TEXT,
                    turno TEXT,
                    quantidade_alunos INTEGER
                )
            ''')
            conn.commit()
    finally:
        release_db_connection(conn)

# Salvar os dados no banco de dados
def salvar_dados_db(dados):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO cadastros (nome, nome_empresa, telefone, cidade, segmento, curso, turno, quantidade_alunos)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', (dados["Nome"], dados["Nome da Empresa"], dados["Telefone"], dados["Cidade"], 
                  dados["Segmento"], dados["Curso"], dados["Turno"], dados["Quantidade de Alunos"]))
            conn.commit()
    finally:
        release_db_connection(conn)

# Obter todos os cadastros
def obter_cadastros():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, nome_empresa, telefone, cidade, segmento, curso, turno, quantidade_alunos FROM cadastros")
            return cur.fetchall()
    finally:
        release_db_connection(conn)

# Excluir um único cadastro
@app.route('/delete/<int:id>', methods=['POST'])
def delete_cadastro(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cadastros WHERE id = %s", (id,))
            conn.commit()
    finally:
        release_db_connection(conn)
    return jsonify({"success": True, "message": "Cadastro excluído com sucesso."})

# Excluir todos os cadastros
@app.route('/delete_all', methods=['POST'])
def delete_all_cadastros():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cadastros")
            conn.commit()
    finally:
        release_db_connection(conn)
    return jsonify({"success": True, "message": "Todos os cadastros foram excluídos."})

# Download da lista em Excel
@app.route('/download_excel')
def download_excel():
    cadastros = obter_cadastros()
    df = pd.DataFrame(cadastros, columns=["ID", "Nome", "Nome da Empresa", "Telefone", "Cidade", "Segmento", "Curso", "Turno", "Quantidade de Alunos"])
    file_path = "cadastros.xlsx"
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    criar_tabela()
    
    if request.method == 'POST':
        nome = request.form['nome']
        nome_empresa = request.form['nome_empresa']
        telefone = request.form['telefone']
        cidade = request.form['cidade']
        segmento = request.form['segmento']
        curso = request.form['curso']
        turno = request.form['turno']
        quantidade_alunos = request.form['quantidade_alunos']

        # Salvar os dados no banco de dados
        dados = {
            "Nome": nome,
            "Nome da Empresa": nome_empresa,
            "Telefone": telefone,
            "Cidade": cidade,
            "Segmento": segmento,
            "Curso": curso,
            "Turno": turno,
            "Quantidade de Alunos": quantidade_alunos
        }
        salvar_dados_db(dados)
        return redirect(url_for('success'))

    return render_template('form.html')

@app.route('/visualizar')
def visualizar():
    cadastros = obter_cadastros()
    return render_template('visualizar.html', cadastros=cadastros)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
