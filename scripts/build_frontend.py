import os
import subprocess
import shutil
import sys
import platform
import tarfile
import requests
from pathlib import Path

def download_file(url, target_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(target_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def install_node():
    """Instala Node.js en el directorio del proyecto"""
    try:
        # Directorio para Node.js
        node_dir = Path('node_installation')
        node_dir.mkdir(exist_ok=True)
        
        # Determinar la arquitectura
        machine = platform.machine().lower()
        if machine in ['x86_64', 'amd64']:
            arch = 'x64'
        elif machine in ['aarch64', 'arm64']:
            arch = 'arm64'
        else:
            raise Exception(f"Arquitectura no soportada: {machine}")

        # URL de Node.js (versión LTS)
        node_version = 'v20.11.1'
        base_url = f'https://nodejs.org/dist/{node_version}'
        if platform.system().lower() == 'linux':
            node_file = f'node-{node_version}-linux-{arch}.tar.xz'
        else:
            raise Exception("Sistema operativo no soportado")

        node_url = f'{base_url}/{node_file}'
        node_path = node_dir / node_file

        print(f"Descargando Node.js desde {node_url}")
        download_file(node_url, node_path)

        print("Extrayendo Node.js...")
        with tarfile.open(node_path) as tar:
            tar.extractall(node_dir)

        # Establecer el PATH para incluir node y npm
        node_bin = node_dir / f'node-{node_version}-linux-{arch}' / 'bin'
        os.environ['PATH'] = f"{node_bin}:{os.environ.get('PATH', '')}"
        
        # Verificar la instalación
        subprocess.run(['node', '--version'], check=True)
        subprocess.run(['npm', '--version'], check=True)
        
        print("Node.js instalado correctamente")
        return True
    except Exception as e:
        print(f"Error instalando Node.js: {e}")
        return False

def build_frontend():
    """Construye el frontend usando Node.js"""
    frontend_dir = Path(__file__).parent.parent / 'frontend'
    dist_dir = frontend_dir / 'dist'
    node_modules = frontend_dir / 'node_modules'
    
    try:
        # Verificar si Node.js está instalado
        try:
            subprocess.run(['node', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Node.js no encontrado, intentando instalar...")
            if not install_node():
                return False
        
        # Instalar dependencias si no existen
        if not node_modules.exists():
            print("Instalando dependencias...")
            subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
        
        # Construir el proyecto
        print("Construyendo el frontend...")
        subprocess.run(['npm', 'run', 'build'], cwd=frontend_dir, check=True)
        
        # Mover los archivos construidos a la carpeta www
        www_dir = frontend_dir.parent / 'www' / 'gatobot' / 'static'
        if dist_dir.exists():
            # Limpiar directorio www si existe
            if www_dir.exists():
                shutil.rmtree(www_dir)
            # Copiar nuevos archivos
            shutil.copytree(dist_dir, www_dir)
            print("Frontend construido y copiado exitosamente")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error durante la construcción: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    
    return False

if __name__ == "__main__":
    build_frontend()
