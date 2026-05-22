# app/db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SCHEMA = 'monitor'  # nome do schema

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def criar_tabela():
    conn = get_conn()
    cur = conn.cursor()
    
    # Cria o schema se não existir
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
    
    # Cria a tabela dentro do schema
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {SCHEMA}.api_logs (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            url TEXT,
            status TEXT,
            codigo_http INTEGER,
            tempo_resposta FLOAT,
            json_valido BOOLEAN,
            horario TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

def salvar_log_db(entrada: dict):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(f'''
            INSERT INTO {SCHEMA}.api_logs
            (nome, url, status, codigo_http, tempo_resposta, json_valido, horario)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (
            entrada.get('nome'),
            entrada.get('url'),
            entrada.get('status'),
            entrada.get('codigo_http'),
            entrada.get('tempo_resposta'),
            entrada.get('json_valido'),
            entrada.get('horario'),
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f'Erro ao salvar no banco: {e}')

def carregar_logs_db(limite=50):
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(f'''
            SELECT nome, url, status, codigo_http, tempo_resposta, json_valido, horario
            FROM {SCHEMA}.api_logs
            ORDER BY horario DESC
            LIMIT %s
        ''', (limite,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {
                'nome': r[0], 'url': r[1], 'status': r[2],
                'codigo_http': r[3], 'tempo_resposta': r[4],
                'json_valido': r[5], 'horario': str(r[6])
            } for r in rows
        ]
    except Exception as e:
        print(f'Erro ao carregar logs: {e}')
        return []