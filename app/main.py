import schedule 
import time
import threading
from config import (API_URLS,MONITORING_INTERVAL, RESPONSE_TIME_THRESHOLD,FLASK_PORT)
from monitor import monitorar_listas
from web import criar_app

def loop_monitoramento():
    
    monitorar_listas(API_URLS)
    schedule.every(MONITORING_INTERVAL).seconds.do(lambda: monitorar_listas(API_URLS))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("==============MONITOR DE APIs INICIADO===============")
    print(F"API CONFIGURADAS: {len(API_URLS)}")
    print(F"INTERVALO DE MONITORAMENTO: {MONITORING_INTERVAL} segundos")
    print(F"THRESHOLD DE TEMPO DE RESPOSTA: {RESPONSE_TIME_THRESHOLD} ms")
    print("=====================================================")


    adicionar = input("Deseja adicionar mais APIs para monitorar? (s/n): ")
    if adicionar.lower() == 's':
        url_extra = input("Digite a URL da API a ser monitorada: ")
        nome_extra = input("Digite o nome da API: ")
        API_URLS.append({"name": nome_extra, "url": url_extra})
        print(F"API {nome_extra} adicionada com sucesso!")


    print("Iniciando monitoramento...")

    t = threading.Thread(target=loop_monitoramento, daemon=True)

    t.start()
    app = criar_app()
    print(F"Servidor web rodando na porta {FLASK_PORT}...")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)    


