import asyncio
import logging
import os
import platform
import threading
from pathlib import Path

import psutil

from core.interfaces.i_infrastructure_initiator import IInfrastructureInitiator
from config.config import BIN_PATH, TOKEN_CLOUDFLARE
from core.logging import Logger


class CloudflaredTunnel(IInfrastructureInitiator):

    logger: logging.Logger
    _cloudflared_path_bin: Path = BIN_PATH / 'cloudflared'
    _thread: threading.Thread
    _loop: asyncio.AbstractEventLoop
    _event: asyncio.Event

    def __init__(self):
        self.logger = Logger('cloudflared_tunnel').get_logger()

    def on_load(self) -> None:
        self.logger.info("Cargando cloudflared tunnel...")
        self._cloudflared_path_bin.mkdir(parents=True, exist_ok=True)
        self._event = asyncio.Event()

    def on_enable(self) -> None:
        self.logger.info("Habilitando cloudflared tunnel...")

        def run_asyncio_loop():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            self._loop.run_until_complete(asyncio.gather(self.on_start(), return_exceptions=True))
            self._loop.close()

        # Iniciar en un hilo
        self._thread = threading.Thread(target=run_asyncio_loop, daemon=True)
        self._thread.start()

    def on_disable(self) -> None:
        self.logger.info("Deshabilitando cloudflared tunnel...")
        self._event.set()
        self.logger.info("cloudflared tunnel deshabilitado.")

    async def on_start(self) -> None:
        self.logger.info("Iniciando cloudflared tunnel...")
        await self.start_cloudflared()

    async def start_cloudflared(self):
        """Inicia el túnel de Cloudflare"""
        retry_count = 0
        max_retries = 3
        retry_delay = 5  # segundos

        try:
            bin_path = BIN_PATH / 'cloudflared'
            bin_path.mkdir(parents=True, exist_ok=True)
            cloudflared_path = bin_path / 'cloudflared-linux-amd64'
            cloudflared_path = str(cloudflared_path)
            if not os.path.exists(cloudflared_path):
                self.logger.error("Cloudflared no encontrado")
                return

            # Hacer el archivo ejecutable
            os.chmod(cloudflared_path, 0o755)

            while not self._event.is_set() and retry_count < max_retries:
                try:
                    # Iniciar cloudflared con token personalizado
                    cloudflared_process = await asyncio.create_subprocess_exec(
                        cloudflared_path,
                        "tunnel",
                        "--no-autoupdate",
                        "run",
                        "--token",
                        TOKEN_CLOUDFLARE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )

                    self.logger.info("Cloudflared tunnel iniciado")

                    # Esperar hasta que el proceso termine o se solicite el cierre
                    while not self._event.is_set():
                        try:
                            # Verificar si el proceso sigue vivo
                            if cloudflared_process.returncode is not None:
                                if retry_count < max_retries:
                                    self.logger.warning(
                                        f"Cloudflared se detuvo, reintento {retry_count + 1}/{max_retries} en {retry_delay} segundos...")
                                    retry_count += 1
                                    await asyncio.sleep(retry_delay)
                                    break
                                else:
                                    self.logger.error("Máximo número de reintentos alcanzado para cloudflared")
                                    return

                            # Leer la salida para evitar que se acumule en el buffer
                            try:
                                stdout_data = await asyncio.wait_for(cloudflared_process.stdout.readline(), timeout=1.0)
                                if stdout_data:
                                    self.logger.debug(f"Cloudflared stdout: {stdout_data.decode().strip()}")
                            except asyncio.TimeoutError:
                                pass

                            await asyncio.sleep(1)
                        except asyncio.CancelledError:
                            break

                    if self._event.is_set():
                        break

                except Exception as e:
                    self.logger.error(f"Error al iniciar cloudflared: {str(e)}")
                    if retry_count < max_retries:
                        retry_count += 1
                        await asyncio.sleep(retry_delay)
                    else:
                        self.logger.error("Máximo número de reintentos alcanzado para cloudflared")
                        break

        except Exception as e:
            self.logger.error(f"Error en cloudflared: {str(e)}")
        finally:
            if cloudflared_process and cloudflared_process.returncode is None:
                try:
                    # Intentar terminar el proceso principal
                    cloudflared_process.terminate()
                    try:
                        await asyncio.wait_for(cloudflared_process.wait(), timeout=5.0)
                    except asyncio.TimeoutError:
                        # Si no se cierra en 5 segundos, forzar el cierre
                        cloudflared_process.kill()
                        await cloudflared_process.wait()

                    # En Linux, buscar y terminar procesos hijo
                    if platform.system() != 'Windows':
                        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                            try:
                                if 'cloudflared' in proc.info['name']:
                                    psutil.Process(proc.info['pid']).terminate()
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass

                    self.logger.info("Cloudflared detenido correctamente")
                except Exception as e:
                    self.logger.error(f"Error al detener cloudflared: {str(e)}")