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


    # if os.getenv("RENDER") is None:
    #     adicionar = input("Deseja adicionar mais APIs para monitorar? (s/n): ")
    #     if adicionar.lower() == 's':
    #         while True:
    #             url_extra = input("URL da API (ou ENTER para finalizar): ")
    #             if not url_extra:
    #                 break
    #             nome_extra = input("Nome da API: ")
    #             API_URLS.append({"name": nome_extra, "url": url_extra})
    #             print(f"API '{nome_extra}' adicionada!")

    print("Iniciando monitoramento...")
    t = threading.Thread(target=loop_monitoramento, daemon=True)
    t.start()
    app = criar_app()
    print(f"Servidor web rodando na porta {FLASK_PORT}...")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)   


