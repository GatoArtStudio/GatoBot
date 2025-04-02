import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Variables de entorno
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.environ.get("DISCORD_REDIRECT_URI")
DISCORD_URL_AUTHORIZE = os.environ.get("DISCORD_URL_AUTHORIZE")
PORT_SERVER_PROXY = os.environ.get("PORT_SERVER_PROXY")
PORT_SERVER_HTTP = os.environ.get("PORT_SERVER_HTTP")
WORKING_MODE = os.environ.get("WORKING_MODE")
SERVER_DEV_ID = os.environ.get("SERVER_DEV_ID")
USER_DEV_ID = os.environ.get("USER_DEV_ID")
TOKEN_CLOUDFLARE = os.environ.get("TOKEN_CLOUDFLARE")
WORKING_MODE_DEV = os.environ.get("WORKING_MODE_DEV")
WORKING_MODE_DEV = True if WORKING_MODE_DEV == 'True' else False
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

# Rutas
SRC_PATH = Path(__file__).resolve().parent.parent
HOME_PATH = SRC_PATH.parent
BIN_PATH = HOME_PATH / '.local'
TMP_PATH = BIN_PATH / 'tmp'

# Crear directorios si no existen
BIN_PATH.mkdir(parents=True, exist_ok=True)
TMP_PATH.mkdir(parents=True, exist_ok=True)

# Servicios API
PAYPAL_API_URL = 'https://api-m.sandbox.paypal.com' if WORKING_MODE_DEV else 'https://api-m.paypal.com'
MUNECRAFT_API_CLIENT_ID = os.environ.get("MUNECRAFT_API_CLIENT_ID")
MUNECRAFT_API_CLIENT_SECRET = os.environ.get("MUNECRAFT_API_CLIENT_SECRET")

RETRY_DELAY = 3  # Tiempo de espera entre intentos, para reconexión del bot con la API de Discord