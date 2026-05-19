import requests
from app.config import WEBHOOK_URL

def enviar_alerta(dados: dict):

    if not WEBHOOK_URL:
        return # Se a URL do webhook não estiver configurada, não envia o alerta
    
    payload = {
        "mensagem": f"ALERTA: {dados['nome']} está com {dados['status']}",
        "url": dados['url'],
        "codigo http": dados.get("codigo_http"),
        "horario":dados["horario"],
    }

    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"Alerta enviado para n8n: {payload['mensagem']}")
    except Exception as e:
        print(f"Erro ao enviar alerta: {e}")