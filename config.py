import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
PORT_SERVER_PROXY = os.environ.get("PORT_SERVER_PROXY")
PORT_SERVER_HTTP = os.environ.get("PORT_SERVER_HTTP")
WORKING_MODE = os.environ.get("WORKING_MODE")
SERVER_DEV_ID = os.environ.get("SERVER_DEV_ID")
USER_DEV_ID = os.environ.get("USER_DEV_ID")
TOKEN_CLOUDFLARE = os.environ.get("TOKEN_CLOUDFLARE")

RETRY_DELAY = 3  # Tiempo de espera entre intentos, para reconexión del bot con la API de Discord