import requests
import time
from datetime import datetime
from logger import salvar_log
from alerts import enviar_alerta
from alerts import enviar_alerta_recuperacao


estado_anterior = {}

def monitorar_api(url: str, nome: str, headers: dict = None):

    inicio = time.time()
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        tempo = round(time.time() - inicio, 3)

        json_valido = True
        try:
            resposta.json()
        except Exception:
            json_valido = False

        if resposta.status_code == 200:
            status = "online"
        elif resposta.status_code in [401, 403]:
            status= "autenticacao falhou"
        elif resposta.status_code >= 500:
            status = "problema no servidor"
        else:
            status = f"offline - http_{resposta.status_code}"


        entrada = {
            "nome": nome,
            "url": url,
            "status": status,
            "codigo_http": resposta.status_code,
            "tempo_resposta": tempo,
            "json_valido": json_valido,
            "horario": horario
        }

    except requests.exceptions.ConnectionError:
        entrada = {
            "nome": nome,
            "url": url,
            "status": "offline - sem conexão",
            "codigo_http": None,
            "tempo_resposta": None,
            "json_valido": None,
            "horario": horario
        }

    except requests.exceptions.Timeout:
        entrada = {
            "nome": nome,
            "url": url,
            "status": "offline - timeout",
            "codigo_http": None,
            "tempo_resposta": None,
            "json_valido": None,
            "horario": horario
        }
            
    salvar_log(entrada)

    status_atual = entrada["status"]
    status_antes = estado_anterior.get(nome)

    if status_atual != "online" and status_antes != status_atual:
        # ficou offline ou mudou o tipo de erro
        enviar_alerta(entrada)
    elif status_atual == "online" and status_antes and status_antes != "online":
        # voltou a ficar online
        enviar_alerta_recuperacao(entrada)

    estado_anterior[nome] = status_atual

    return entrada


def monitorar_listas(apis: list):

    resultados = []
    for api in apis:
        resultado = monitorar_api(api["url"], api["name"])
        resultados.append(resultado)
        print(f"{resultado['horario']} - {resultado['nome']} - {resultado['status']} - {resultado['tempo_resposta']}s")
    return resultados