import os
import psycopg2
import pandas as pd
from psycopg2 import pool
from flask import Flask, render_template, request, redirect, url_for, send_file

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

# Obter cadastros com paginação
def obter_cadastros(pagina, registros_por_pagina=14):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM cadastros")
            total_registros = cur.fetchone()[0]
            
            offset = (pagina - 1) * registros_por_pagina
            cur.execute("SELECT id, nome, nome_empresa, telefone, cidade, segmento, curso, turno, quantidade_alunos FROM cadastros ORDER BY id LIMIT %s OFFSET %s", (registros_por_pagina, offset))
            return cur.fetchall(), total_registros
    finally:
        release_db_connection(conn)

@app.route('/')
def index():
    criar_tabela()
    return render_template('form.html')

@app.route('/visualizar')
def visualizar():
    pagina = int(request.args.get('pagina', 1))
    cadastros, total_registros = obter_cadastros(pagina)
    total_paginas = (total_registros // 14) + (1 if total_registros % 14 else 0)
    return render_template('visualizar.html', cadastros=cadastros, pagina=pagina, total_paginas=total_paginas)

@app.route('/baixar_excel')
def baixar_excel():
    conn = get_db_connection()
    try:
        df = pd.read_sql("SELECT * FROM cadastros", conn)
        caminho_arquivo = "cadastros.xlsx"
        df.to_excel(caminho_arquivo, index=False)
        return send_file(caminho_arquivo, as_attachment=True)
    finally:
        release_db_connection(conn)

@app.route('/excluir_todos', methods=['POST'])
def excluir_todos():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cadastros")
            conn.commit()
    finally:
        release_db_connection(conn)
    return redirect(url_for('visualizar'))

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cadastros WHERE id = %s", (id,))
            conn.commit()
    finally:
        release_db_connection(conn)
    return redirect(url_for('visualizar'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
