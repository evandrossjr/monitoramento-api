import os
from dotenv import load_dotenv

load_dotenv()

API_URLS = [
    {
        "name": os.getenv("API_NAME"),
        "url": os.getenv("API_URL")
    }
]

WEBHOOK_URL = os.getenv("WEBHOOK_URL", '')
MONITORING_INTERVAL = int(os.getenv("MONITORING_INTERVAL", 60))
RESPONSE_TIME_THRESHOLD = int(os.getenv("RESPONSE_TIME_THRESHOLD", 500))
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
