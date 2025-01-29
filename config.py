import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get("TOKEN")
PORT_SERVER_PROXY = os.environ.get("PORT_SERVER_PROXY")