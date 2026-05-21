import schedule 
import time
import threading
from config import (API_URLS, MONITORING_INTERVAL, RESPONSE_TIME_THRESHOLD, FLASK_PORT)
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
    print(f"API CONFIGURADAS: {len(API_URLS)}")
    print(f"INTERVALO DE MONITORAMENTO: {MONITORING_INTERVAL} segundos")
    print(f"THRESHOLD DE TEMPO DE RESPOSTA: {RESPONSE_TIME_THRESHOLD} ms")
    print("=====================================================")

    print("Iniciando monitoramento...")

    # Flask em thread separada
    app = criar_app()
    t_flask = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=FLASK_PORT, debug=False),
        daemon=False
    )
    t_flask.start()
    print(f"Servidor web rodando na porta {FLASK_PORT}...")

    # Loop principal — mantém o processo vivo no Render
    loop_monitoramento()