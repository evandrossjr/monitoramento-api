# 🔴 Monitor de APIs

Sistema automatizado de monitoramento de APIs com alertas inteligentes via Telegram, análise por IA e dashboard web.

---

## 📌 Sobre o Projeto

Sistema desenvolvido em Python que monitora continuamente a disponibilidade de APIs e sites, registra o histórico em banco de dados PostgreSQL, envia alertas automáticos via n8n + Telegram quando algum serviço apresenta problema, e exibe tudo em um dashboard web com autenticação.

---

## 🏗️ Arquitetura

```
Python Monitor (Flask)
        │
        ├── Verifica APIs a cada 60s
        ├── Salva logs no PostgreSQL (Railway)
        ├── Envia webhook ao n8n se houver falha
        │
        └── n8n (Render)
                │
                ├── Recebe o webhook
                ├── Filtra: status != online
                ├── Groq AI analisa o incidente
                └── Telegram notifica o time
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12 + Flask |
| Monitoramento | Requests + Schedule |
| Banco de dados | PostgreSQL (Railway) |
| Automação | n8n |
| IA | Groq (LLaMA 3.3) |
| Notificação | Telegram Bot |
| Deploy | Render |
| Segurança | Variáveis de ambiente + Session Auth |

---

## 📁 Estrutura do Projeto

```
monitoramento-api/
│
├── app/
│   ├── main.py         # entrada principal, loop de monitoramento
│   ├── monitor.py      # lógica de verificação HTTP
│   ├── alerts.py       # envio de webhooks ao n8n
│   ├── logger.py       # registro em JSON e PostgreSQL
│   ├── db.py           # conexão e operações no banco
│   ├── config.py       # variáveis de ambiente
│   └── web.py          # servidor Flask + autenticação
│
├── templates/
│   ├── index.html      # dashboard
│   └── login.html      # tela de login
│
├── logs/
│   ├── api_logs.json   # backup local dos logs
│   └── errors.log      # erros graves
│
├── .env                # variáveis sensíveis (não versionar)
├── .gitignore
├── requirements.txt
├── Procfile
└── run.py              # ponto de entrada para o Render
```

---

## ⚙️ Funcionalidades

- ✅ Monitoramento contínuo com intervalo configurável
- ✅ Detecção de: timeout, erro HTTP, falha de autenticação, offline
- ✅ Alerta quando API **cai** e quando **volta ao ar**
- ✅ Análise automática do incidente por IA (Groq)
- ✅ Notificação no Telegram com diagnóstico e recomendação
- ✅ Dashboard web com login e senha
- ✅ Histórico persistido no PostgreSQL
- ✅ Health check público para UptimeRobot

---

## 🚀 Como Executar Localmente

**1. Clonar o repositório**
```bash
git clone https://github.com/evandrossjr/monitoramento-api.git
cd monitoramento-api
```

**2. Criar e ativar o ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Instalar dependências**
```bash
pip install -r requirements.txt
```

**4. Configurar o `.env`**
```env
API_1_URL=https://jsonplaceholder.typicode.com/posts
API_1_NAME=JSONPlaceholder

WEBHOOK_URL=https://seu-n8n.onrender.com/webhook/seu-id
MONITOR_INTERVAL=60
FLASK_PORT=5000

ADMIN_USER=admin
ADMIN_PASSWORD=sua-senha
SECRET_KEY=sua-chave-secreta

DATABASE_URL=postgresql://usuario:senha@host:porta/railway
```

**5. Rodar**
```bash
python run.py
```

Acesse: `http://localhost:5000`

---

## ☁️ Deploy

### Python → Render
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python run.py`
- **Porta:** `10000`
- Adicionar todas as variáveis do `.env` em **Environment**

### n8n → Render
- **Imagem Docker:** `n8nio/n8n`
- **Porta:** `5678`
- Variáveis necessárias: `DB_TYPE`, `DB_POSTGRESDB_*`, `N8N_ENCRYPTION_KEY`, `WEBHOOK_URL`

### Banco → Railway
- PostgreSQL com schema `monitor`
- Tabela `monitor.api_logs` criada automaticamente na primeira execução

---

## 🔔 Fluxo de Alerta no n8n

```
Webhook (POST) → IF status != "online" → Basic LLM Chain (Groq) → Telegram
```

Exemplo de mensagem recebida no Telegram:

```
🚨 Incidente detectado
📌 API: Todo List App
📊 Status: OFFLINE - TIMEOUT
🕐 Horário: 2026-05-20 23:36:14
🔍 Causa provável: Serviço em cold start ou instabilidade no servidor
✅ Ação recomendada: Verificar logs do Render e aguardar recuperação automática
```

---

## 🔐 Segurança

- Credenciais em variáveis de ambiente (nunca no código)
- Dashboard protegido por login e senha via sessão Flask
- Comunicação com banco via SSL (`sslmode=require`)
- Webhook com ID aleatório de difícil adivinhação
- `.env` e `venv/` no `.gitignore`

---

## 📊 Banco de Dados

Schema: `monitor`  
Tabela: `api_logs`

| Campo | Tipo | Descrição |
|---|---|---|
| id | SERIAL | Chave primária |
| nome | TEXT | Nome da API |
| url | TEXT | Endereço monitorado |
| status | TEXT | online / offline / timeout |
| codigo_http | INTEGER | Código de resposta HTTP |
| tempo_resposta | FLOAT | Tempo em segundos |
| json_valido | BOOLEAN | Se retornou JSON válido |
| horario | TIMESTAMP | Data e hora da verificação |

---

## 📦 Dependências

```
requests
httpx
python-dotenv
schedule
flask
flask-cors
psycopg2-binary
```

---

## 📅 Cronograma de Desenvolvimento

| Dia | Entregas |
|---|---|
| 1 | Estrutura, consumo de API, logs JSON |
| 2 | Monitoramento contínuo, condicionais, tratamento de erros |
| 3 | Integração n8n, alertas Telegram |
| 4 | IA (Groq), análise automática de incidentes |
| 5 | Docker, banco PostgreSQL, deploy, dashboard com login |

---

## 👤 Autor
Evandro Sacramento  
Desenvolvido como projeto da matéria Programação Aplicada em Python.  
Demonstra: Python · APIs HTTP · JSON · Flask · n8n · PostgreSQL · IA · Docker · Deploy
