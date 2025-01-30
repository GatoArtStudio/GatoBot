import yaml
import time
import logging
import secrets
from pathlib import Path
from collections import defaultdict
from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse
from log.logging_config import setup_logging
from config import PORT_SERVER_HTTP

# Instancia el debug
setup_logging()
logger = logging.getLogger(__name__)

class ServerHTTP:
    def __init__(self):
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory='www/templates')
        self.app.mount("/static", StaticFiles(directory="www/static"), name="static")
        self.upload_dir = Path("www/uploads")
        self.upload_dir.mkdir(exist_ok=True)
        self.setup_routes()
        self.cookies = {}
        self.users = {}
        self.load_users()
        self.failed_attempts = defaultdict(int)
        self.locked_accounts = {}
    
    def load_users(self):
        '''
        Carga los usuarios y contraseñas desde un archivo
        '''
        try:
            with open("users.yaml", "r") as f:
                d = yaml.safe_load(f)
                self.users = d['users']
        except Exception as e:
            logger.error(f"Error loading users: {e}")
    
    def setup_routes(self):
        '''
        Iniciamos todas las rutas de la aplicación
        '''

        # pagina principal de la aplicación
        @self.app.get("/")
        async def home(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})
        
        # pagina de login
        @self.app.post("/login")
        async def login(responde: Response, request: Request, username: str = Form(...), password: str = Form(...)):
            # verificamos si el usuario esta bloqueado
            if username in self.locked_accounts:
                lock_time = self.locked_accounts[username]
                if time.time() - lock_time < 300: # 5 minutos
                    return RedirectResponse(url="/", status_code=302)
                else:
                    del self.locked_accounts[username]

            # verificamos si el usuario y contraseña son correctos
            if username in self.users and self.users[username] == password:
                session_token = secrets.token_hex(32)
                responde = RedirectResponse(url="/dashboard", status_code=302)
                responde.set_cookie(key="session", value=session_token, httponly=True)
                self.cookies[session_token] = username
                self.failed_attempts[username] = 0
                return responde
            else:
                self.failed_attempts[username] += 1
                if self.failed_attempts[username] > 5: # 5 intentos fallidos
                    self.locked_accounts[username] = time.time()
                    logger.warning(f"Account {username} locked, ip: {request.client.host}")
                return RedirectResponse(url="/", status_code=302)
        
        @self.app.get("/dashboard")
        async def dashboard(request: Request):
            session = request.cookies.get('session')
            # verificamos si la sesión es valida
            if session is None or session not in self.cookies:
                return RedirectResponse(url="/", status_code=302)
            
            files = [f.name for f in self.upload_dir.iterdir() if f.is_file()]
            return self.templates.TemplateResponse("dashboard.html", {"request": request, "files": files})

        @self.app.post("/upload")
        async def upload(request: Request, file: UploadFile = File(...)):
            session = request.cookies.get('session')
            # verificamos si la sesión es valida
            if session is None or session not in self.cookies:
                return RedirectResponse(url="/", status_code=302)
            
            file_path = self.upload_dir / file.filename
            with file_path.open('wb') as f:
                f.write(await file.read())

            return RedirectResponse(url="/dashboard", status_code=302)

        @self.app.get("/download/{filename}")
        async def download(filename: str, request: Request):
            session = request.cookies.get('session')
            # verificamos si la sesión es valida
            if session is None or session not in self.cookies:
                return RedirectResponse(url="/", status_code=302)
            
            file_path = self.upload_dir / filename
            if not file_path.is_file():
                return RedirectResponse(url="/dashboard", status_code=302)
            
            if file_path.exists() and file_path.is_file():
                return FileResponse(str(file_path))
            else:
                return {"message": "File not found"}


    def start_server(self):
        import uvicorn
        uvicorn.run(self.app, host='0.0.0.0', port=int(PORT_SERVER_HTTP))