from flask import Flask, jsonify, render_template, redirect, url_for, request, session
from flask_cors import CORS
from functools import wraps
from logger import carregar_logs
from monitor import monitorar_api
from config import API_URLS, SECRET_KEY, ADMIN_USER, ADMIN_PASSWORD
import os
 
def criar_app():
    # Aponta para a pasta templates/ na raiz do projeto
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'templates')
    )
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = SECRET_KEY
    CORS(app)
 
    # Decorator de protecao de rotas
    def login_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get('logado'):
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated
 
    # Rota de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if session.get('logado'):
            return redirect(url_for('index'))
        if request.method == 'POST':
            user = request.form.get('usuario')
            pwd = request.form.get('senha')
            if user == ADMIN_USER and pwd == ADMIN_PASSWORD:
                session['logado'] = True
                return redirect(url_for('index'))
            return render_template('login.html', erro='Usuario ou senha incorretos')
        return render_template('login.html', erro=None)
 
    # Rota de logout
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
 
    # Dashboard — protegido
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')
 
    # API de logs — protegida
    @app.route('/api/logs')
    @login_required
    def get_logs():
        logs = carregar_logs()
        return jsonify(logs[-50:])
 
    # API de verificacao manual — protegida
    @app.route('/api/checar')
    @login_required
    def checar_agora():
        resultados = []
        for api in API_URLS:
            r = monitorar_api(api['url'], api['name'])
            resultados.append(r)
        return jsonify(resultados)
 
    # API de status resumo — protegida
    @app.route('/api/status')
    @login_required
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
 
    # Health check — publico (para UptimeRobot e Render)
    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200
 
    return app