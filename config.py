import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
PORT_SERVER_PROXY = os.environ.get("PORT_SERVER_PROXY")
PORT_SERVER_HTTP = os.environ.get("PORT_SERVER_HTTP")