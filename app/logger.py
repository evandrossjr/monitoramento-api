import json
import os
import logging
from datetime import datetime
 
# Importa o banco — se nao tiver DATABASE_URL configurado, ignora
try:
    from db import salvar_log_db, criar_tabela
    criar_tabela()  # cria a tabela se nao existir
    USE_DB = True
except Exception:
    USE_DB = False
 
os.makedirs('logs', exist_ok=True)
 
logging.basicConfig(
    filename='logs/errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
 
def salvar_log(entrada: dict):
    # Salva no banco se disponivel
    if USE_DB:
        salvar_log_db(entrada)
 
    # Salva no arquivo JSON local (backup)
    arquivo = 'logs/api_logs.json'
    historico = []
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            try:
                historico = json.load(f)
            except:
                historico = []
    historico.append(entrada)
    historico = historico[-500:]
    with open(arquivo, 'w') as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)
 
def carregar_logs():
    # Carrega do banco se disponivel
    if USE_DB:
        try:
            from db import carregar_logs_db
            return carregar_logs_db(50)
        except:
            pass
 
    # Fallback: arquivo local
    arquivo = 'logs/api_logs.json'
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, 'r') as f:
        try:
            return json.load(f)
        except:
            return []