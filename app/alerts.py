import time as time_module

import requests
from config import WEBHOOK_URL

def enviar_alerta(dados: dict):
    if not WEBHOOK_URL:
        return

    payload = {
        "nome": dados["nome"],
        "mensagem": f"ALERTA: {dados['nome']} está com {dados['status']}",
        "url": dados["url"],
        "status": dados["status"],
        "codigo_http": dados.get("codigo_http"),
        "tempo_resposta": dados.get("tempo_resposta"),
        "horario": dados["horario"],
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"  Alerta enviado para n8n: {payload['mensagem']}")
        time_module.sleep(5)
    except Exception as e:
        print(f"  Erro ao enviar alerta: {e}")


def enviar_alerta_recuperacao(dados: dict):
    if not WEBHOOK_URL:
        return

    payload = {
        "nome": dados["nome"],
        "mensagem": f"RECUPERADO: {dados['nome']} voltou a ficar online",
        "url": dados["url"],
        "status": "online",
        "codigo_http": dados.get("codigo_http"),
        "tempo_resposta": dados.get("tempo_resposta"),
        "horario": dados["horario"],
        "recuperado": True
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"  Recuperação enviada para n8n: {payload['mensagem']}")
        time_module.sleep(5)
    except Exception as e:
        print(f"  Erro ao enviar recuperação: {e}")