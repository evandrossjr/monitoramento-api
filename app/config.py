import os
from dotenv import load_dotenv

load_dotenv()

API_URLS = []

i = 1
while True:
    url = os.getenv(f"API_{i}_URL")
    name = os.getenv(f"API_{i}_NAME")
    if not url:
        break
    API_URLS.append({"url": url, "name": name})
    i += 1

    
WEBHOOK_URL = os.getenv("WEBHOOK_URL", '')
MONITORING_INTERVAL = int(os.getenv("MONITORING_INTERVAL", 60))
RESPONSE_TIME_THRESHOLD = int(os.getenv("RESPONSE_TIME_THRESHOLD", 500))
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
