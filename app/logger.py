import os
import logging
import json
from datetime import datetime


# Para criar o diretório de logs, se não existir
os.makedirs('logs', exist_ok=True)


logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def salvar_log(entrada: dict):
    arquivo = 'logs/api_logs.json'
    historico = []

    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            try:
                historico = json.load(f)
            except json.JSONDecodeError:
                historico = []  # Se o arquivo estiver vazio ou corrompido, inicia um novo histórico

    historico.append(entrada)


    historico = historico[-500:]

    with open(arquivo, 'w') as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)


def carregar_logs():

    arquivo = 'logs/api_logs.json'
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
        


