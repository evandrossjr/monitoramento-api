from flask import Flask, jsonify, render_template
from flask_cors import CORS
from logger import carregar_logs
from monitor import monitorar_api
from config import API_URLS
 
def criar_app():
    app = Flask(__name__)
    CORS(app)
 
    @app.route('/')
    def index():
        return render_template('index.html')
 
    @app.route('/api/logs')
    def get_logs():
        logs = carregar_logs()
        return jsonify(logs[-50:])  # ultimos 50
 
    @app.route('/api/checar')
    def checar_agora():
        resultados = []
        for api in API_URLS:
            r = monitorar_api(api['url'], api['name'])
            resultados.append(r)
        return jsonify(resultados)
 
    @app.route('/api/status')
    def status_resumo():
        logs = carregar_logs()
        total = len(logs)
        online = sum(1 for l in logs if l.get('status') == 'online')
        return jsonify({
            'total_verificacoes': total,
            'online': online,
            'offline': total - online,
            'taxa_sucesso': round(online / total * 100, 1) if total else 0
        })
    
    
 
    return app