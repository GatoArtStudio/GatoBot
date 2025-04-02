from __future__ import annotations

import asyncio
import logging
import os
import subprocess
import threading
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.routes.routes_auth_discord import RoutesAuthDiscord
from config.config import SRC_PATH
from helpers.herlpers_network import HerlpersNetwork
from core.interfaces.i_infrastructure_initiator import IInfrastructureInitiator
from api.routes.routes_api_rest import BotApi
from core.logging import Logger


class ServidorWeb(IInfrastructureInitiator, HerlpersNetwork):

    logger: logging.Logger
    _app: FastAPI
    _process: any
    _shutdown_event: asyncio.Event
    _thread: threading.Thread
    _host_server: str
    _port_server: int
    _frontend_path: Path

    def __init__(
            self,
            host: str = '0.0.0.0',
            port: int = 25978,
            frontend_path: str = 'gatobot'
    ):
        self.logger = Logger('servidor_web').get_logger()

        # Configuración de recursos del servidor
        self._host_server = host
        self._port_server = port

        # Configuración de la web
        self._frontend_path = SRC_PATH / 'frontend' / frontend_path

    def on_load(self) -> None:
        self.logger.info("Cargando servidor web...")
        self._shutdown_event = asyncio.Event()

        # Configuración de FastAPI
        self._app = FastAPI()
        routes_api_bot = BotApi()
        routes_auth_discord = RoutesAuthDiscord()
        self._app.include_router(routes_api_bot.router)
        self._app.include_router(routes_auth_discord.router)

        # Configurar CORS
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Montamos archivos estáticos para la web
        frontend_public =  self._frontend_path / 'dist'
        self._app.mount(
            "/",
            StaticFiles(
                directory=f'{frontend_public}',
                html=True
            ),
            name="static"
        )
        self.logger.info(f'Ruta de archivos estáticos para la web: {frontend_public}')


    def on_enable(self) -> None:
        self.logger.info("Habilitando servidor web...")

        def run_server():
            """Inicia el servidor web en un hilo separado."""
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(
                asyncio.gather(
                    self.main(),
                    return_exceptions=True
                )
            )
            loop.close()

        try:
            self._thread = threading.Thread(
                target=run_server,
                daemon=True
            )
            self._thread.start()
        except Exception as e:
            self.logger.error(f"Error al iniciar el servidor web: {str(e)}")

    def on_disable(self) -> None:
        self.logger.info("Deshabilitando servidor web...")
        self._shutdown_event.set()
        self.logger.info("Servidor web desabilitado.")

    async def start_web_server(self):
        config = uvicorn.Config(
            self._app,
            host=self._host_server,
            port=self._port_server,
            log_level="info"
        )
        server = uvicorn.Server(config)
        self._process = await server.serve()

    async def main(self):
        self.logger.info("Iniciando servidor web...")
        try:
            # Construir el frontend
            if not self.build_frontend():
                self.logger.error("Error construyendo el frontend")
                return

            # Iniciar servicios
            await self.start_web_server()
        except KeyboardInterrupt:
            return
        except Exception as e:
            self.logger.error(f"Error en el programa principal: {str(e)}")
        finally:
            # Asegurarse de que todo se cierre correctamente
            return

    def build_frontend(self) -> bool | None:
        """
        Construye el frontend usando Node.js
        """
        try:
            self.logger.info("Construyendo el frontend...")

            # Verificar que tenemos las rutas a los binarios
            if 'NODE_BINARY' not in os.environ or 'NPM_BINARY' not in os.environ:
                if not self.install_node():
                    return False

            # Obtener las rutas a los binarios
            npm_binary = os.environ['NPM_BINARY']

            # Preparar el entorno con el PATH actualizado
            env = os.environ.copy()
            bin_dir = str(Path(os.environ['NODE_BINARY']).parent)
            env['PATH'] = f"{bin_dir}:{env.get('PATH', '')}"

            # Instalar dependencias
            self.logger.info("Instalando dependencias del frontend...")
            subprocess.run([npm_binary, 'install'],
                           cwd=self._frontend_path,
                           env=env,
                           check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            timeout=600  # 10 minutos
            )

            # Construir el proyecto
            self.logger.info("Construyendo el proyecto frontend...")
            subprocess.run([npm_binary, 'run', 'build'],
                           cwd=self._frontend_path,
                           env=env,
                           check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            timeout=600  # 10 minutos
           )

            # Copiar archivos construidos
            dist_dir = self._frontend_path / 'dist'

            # Copiar archivos
            if dist_dir.exists():

                self.logger.info("Frontend construido y copiado exitosamente")
                return True
            else:
                self.logger.error("No se encontró el directorio dist")
                return False

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error en el comando npm: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado: {str(e)}")
            return False