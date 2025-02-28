import sys
import socket
import aiohttp
import asyncio
import uvicorn
import platform
import tarfile
import requests
import signal
import psutil
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from base.bot import bot
from config import RETRY_DELAY, TOKEN_CLOUDFLARE, TOKEN
from log import Logger
from api.routes import router as api_router
import subprocess
import os
import shutil

# Configuración de logging
logger = Logger().get_logger()

# Variables globales para control de servicios
shutdown_event = asyncio.Event()
server_process = None
cloudflared_process = None

# Configuración de FastAPI
app = FastAPI()
app.include_router(api_router)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_file(url, target_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(target_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def install_node():
    """Instala Node.js en el directorio del proyecto"""
    try:
        # Directorio para Node.js - usar un directorio en el home del usuario actual
        home = os.path.expanduser("~")
        node_dir = Path(home) / '.local' / 'node_installation'
        node_dir.mkdir(parents=True, exist_ok=True)
        
        # Determinar la arquitectura
        machine = platform.machine().lower()
        if machine in ['x86_64', 'amd64']:
            arch = 'x64'
        elif machine in ['aarch64', 'arm64']:
            arch = 'arm64'
        else:
            raise Exception(f"Arquitectura no soportada: {machine}")

        # URL de Node.js (versión LTS)
        node_version = 'v22.14.0'
        base_url = f'https://nodejs.org/dist/{node_version}'
        if platform.system().lower() == 'linux':
            node_file = f'node-{node_version}-linux-{arch}.tar.xz'
        else:
            raise Exception("Sistema operativo no soportado")

        # Descargar Node.js si no existe
        node_path = node_dir / node_file
        if not node_path.exists():
            logger.info(f"Descargando Node.js desde {base_url}/{node_file}")
            download_file(f"{base_url}/{node_file}", node_path)

        # Extraer Node.js
        logger.info("Extrayendo Node.js...")
        extracted_dir = node_dir / f'node-{node_version}-linux-{arch}'
        
        # Si el directorio ya existe, lo eliminamos
        if extracted_dir.exists():
            import shutil
            shutil.rmtree(str(extracted_dir))
        
        with tarfile.open(node_path) as tar:
            def is_within_directory(directory, target):
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
                prefix = os.path.commonprefix([abs_directory, abs_target])
                return prefix == abs_directory
                
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted path traversal in tar file")
                
                tar.extractall(path, members, numeric_owner=numeric_owner)
                
            safe_extract(tar, str(node_dir))

        # Obtener el directorio bin
        bin_dir = extracted_dir / 'bin'
        node_binary = str(bin_dir / 'node')
        npm_script = str(bin_dir / 'npm')

        # Crear script envoltorio para npm
        wrapper_dir = node_dir / 'wrappers'
        wrapper_dir.mkdir(exist_ok=True)
        
        npm_wrapper = wrapper_dir / 'npm'
        with open(npm_wrapper, 'w') as f:
            f.write(f'''#!/bin/sh
export PATH="{bin_dir}:$PATH"
export NODE_PATH="{extracted_dir}/lib/node_modules"
"{node_binary}" "{npm_script}" "$@"
''')

        # Intentar hacer ejecutables los archivos necesarios
        try:
            os.chmod(str(npm_wrapper), 0o755)
            os.chmod(node_binary, 0o755)
            os.chmod(npm_script, 0o755)
        except Exception as e:
            logger.warning(f"No se pudieron establecer permisos ejecutables: {e}")
            # Continuamos aunque no se puedan establecer los permisos

        # Verificar la instalación
        try:
            # Verificar node
            result = subprocess.run([node_binary, '--version'], 
                                 check=True, 
                                 capture_output=True, 
                                 text=True)
            logger.info(f"Node.js verificado correctamente: {result.stdout.strip()}")
            
            # Verificar npm usando el wrapper
            result = subprocess.run(['sh', str(npm_wrapper), '--version'], 
                                 check=True, 
                                 capture_output=True, 
                                 text=True)
            logger.info(f"npm verificado correctamente: {result.stdout.strip()}")
            
            # Guardar las rutas
            os.environ['NODE_BINARY'] = node_binary
            os.environ['NPM_BINARY'] = str(npm_wrapper)
            os.environ['NODE_PATH'] = f"{extracted_dir}/lib/node_modules"
            os.environ['PATH'] = f"{bin_dir}:{os.environ.get('PATH', '')}"
            
            logger.info("Node.js instalado y configurado correctamente")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error verificando la instalación: {str(e)}")
            if e.stdout:
                logger.error(f"Stdout: {e.stdout}")
            if e.stderr:
                logger.error(f"Stderr: {e.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error instalando Node.js: {str(e)}")
        return False

def build_frontend():
    """Construye el frontend usando Node.js"""
    try:
        logger.info("Construyendo el frontend...")
        
        # Verificar que tenemos las rutas a los binarios
        if 'NODE_BINARY' not in os.environ or 'NPM_BINARY' not in os.environ:
            if not install_node():
                return False
        
        frontend_dir = Path('frontend')
        npm_binary = os.environ['NPM_BINARY']
        
        # Preparar el entorno con el PATH actualizado
        env = os.environ.copy()
        bin_dir = str(Path(os.environ['NODE_BINARY']).parent)
        env['PATH'] = f"{bin_dir}:{env.get('PATH', '')}"
        
        # Instalar dependencias
        logger.info("Instalando dependencias del frontend...")
        subprocess.run([npm_binary, 'install'], 
                      cwd=frontend_dir,
                      env=env,
                      check=True)
        
        # Construir el proyecto
        logger.info("Construyendo el proyecto frontend...")
        subprocess.run([npm_binary, 'run', 'build'], 
                      cwd=frontend_dir,
                      env=env,
                      check=True)
        
        # Copiar archivos construidos
        dist_dir = frontend_dir / 'dist'
        static_dir = Path('www/gatobot/static')
        
        # Crear directorio si no existe
        static_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar archivos
        if dist_dir.exists():
            for item in dist_dir.glob('*'):
                if item.is_file():
                    shutil.copy2(item, static_dir)
                else:
                    dest = static_dir / item.name
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(item, dest)
            
            logger.info("Frontend construido y copiado exitosamente")
            return True
        else:
            logger.error("No se encontró el directorio dist")
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Error en el comando npm: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return False

# Montar archivos estáticos
app.mount("/", StaticFiles(directory="www/gatobot/static", html=True), name="static")

async def start_cloudflared():
    """Inicia el túnel de Cloudflare"""
    global cloudflared_process
    retry_count = 0
    max_retries = 3
    retry_delay = 5  # segundos

    try:
        cloudflared_path = "./cloudflared-linux-amd64"
        if not os.path.exists(cloudflared_path):
            logger.error("Cloudflared no encontrado")
            return

        # Hacer el archivo ejecutable
        os.chmod(cloudflared_path, 0o755)
        
        while not shutdown_event.is_set() and retry_count < max_retries:
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
                
                logger.info("Cloudflared tunnel iniciado")
                
                # Esperar hasta que el proceso termine o se solicite el cierre
                while not shutdown_event.is_set():
                    try:
                        # Verificar si el proceso sigue vivo
                        if cloudflared_process.returncode is not None:
                            if retry_count < max_retries:
                                logger.warning(f"Cloudflared se detuvo, reintento {retry_count + 1}/{max_retries} en {retry_delay} segundos...")
                                retry_count += 1
                                await asyncio.sleep(retry_delay)
                                break
                            else:
                                logger.error("Máximo número de reintentos alcanzado para cloudflared")
                                return
                        
                        # Leer la salida para evitar que se acumule en el buffer
                        try:
                            stdout_data = await asyncio.wait_for(cloudflared_process.stdout.readline(), timeout=1.0)
                            if stdout_data:
                                logger.debug(f"Cloudflared stdout: {stdout_data.decode().strip()}")
                        except asyncio.TimeoutError:
                            pass

                        await asyncio.sleep(1)
                    except asyncio.CancelledError:
                        break
                
                if shutdown_event.is_set():
                    break

            except Exception as e:
                logger.error(f"Error al iniciar cloudflared: {str(e)}")
                if retry_count < max_retries:
                    retry_count += 1
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error("Máximo número de reintentos alcanzado para cloudflared")
                    break
                
    except Exception as e:
        logger.error(f"Error en cloudflared: {str(e)}")
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
                
                logger.info("Cloudflared detenido correctamente")
            except Exception as e:
                logger.error(f"Error al detener cloudflared: {str(e)}")

async def start_web_server():
    global server_process
    config = uvicorn.Config(app, host="0.0.0.0", port=25978, log_level="info")
    server = uvicorn.Server(config)
    server_process = await server.serve()

async def check_internet_connection() -> bool:
    target_host = 'https://discord.com'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.head(target_host) as res:
                return res.status == 200
        except aiohttp.ClientError as e:
            logger.error(e)
            return False

async def handle_bot_connection():
    try:
        logger.info("Estableciendo conexion...")
        async with bot:
            await bot.start(TOKEN)
    except KeyboardInterrupt:
        await handle_shutdown()
    except (socket.gaierror, aiohttp.client_exceptions.ClientConnectorError, RuntimeError):
        logger.error("Conexion cerrada por error de red.")
        if await check_internet_connection():
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        sys.exit(2)

async def handle_shutdown():
    """Maneja el cierre ordenado de todos los servicios"""
    logger.info("\n¡Hasta luego! Deteniendo servicios...")
    
    # Señalizar a todos los servicios que deben detenerse
    shutdown_event.set()
    
    # Detener el bot
    if not bot.is_closed():
        await bot.close()
        logger.info("Bot desconectado correctamente")
    
    # Detener el servidor web
    if server_process and server_process.returncode is None:
        server_process.terminate()
        logger.info("Servidor web detenido")
    
    # Esperar a que cloudflared se detenga
    if cloudflared_process and cloudflared_process.returncode is None:
        cloudflared_process.terminate()
        try:
            await asyncio.wait_for(cloudflared_process.wait(), timeout=5.0)
            logger.info("Cloudflared detenido correctamente")
        except asyncio.TimeoutError:
            cloudflared_process.kill()
            await cloudflared_process.wait()
            logger.info("Cloudflared forzado a detenerse")
    
    logger.info("¡Todos los servicios han sido detenidos correctamente!")

def setup_signal_handlers():
    """Configura los manejadores de señales para cierre ordenado"""
    def signal_handler(sig, frame):
        logger.info("\nSeñal de interrupción recibida...")
        asyncio.create_task(handle_shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    try:
        setup_signal_handlers()
        
        # Construir el frontend
        if not build_frontend():
            logger.error("Error construyendo el frontend")
            return
        
        # Iniciar servicios
        services = [
            handle_bot_connection(),
            start_cloudflared(),
            start_web_server()
        ]
        
        # Esperar a que los servicios terminen o se solicite el cierre
        await asyncio.gather(*services, return_exceptions=True)
        
    except KeyboardInterrupt:
        await handle_shutdown()
    except Exception as e:
        logger.error(f"Error en el programa principal: {str(e)}")
    finally:
        # Asegurarse de que todo se cierre correctamente
        await handle_shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass  # El cierre ya fue manejado por handle_shutdown
    except Exception as e:
        logger.error(f"Error fatal: {str(e)}")
    finally:
        logger.info("¡Gracias por usar GatoBot! ¡Hasta la próxima! 😺")