import logging
import os
import platform
import subprocess
import tarfile
from abc import ABC

import requests

from config.config import HOME_PATH


class HerlpersNetwork(ABC):

    logger: logging.Logger

    def download_file(self, url: str, target_path: str) -> None:
        """
        Descarga un archivo desde una URL y lo guarda en un archivo local.
        """
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def install_node(self):
        """Instala Node.js en el directorio del proyecto"""
        try:
            # Directorio para Node.js - usar un directorio en el home del usuario actual
            home = HOME_PATH
            node_dir = home / '.local' / 'node_installation'
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
                self.logger.info(f"Descargando Node.js desde {base_url}/{node_file}")
                self.download_file(f"{base_url}/{node_file}", node_path)

            # Extraer Node.js
            self.logger.info("Extrayendo Node.js...")
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
                self.logger.warning(f"No se pudieron establecer permisos ejecutables: {e}")
                # Continuamos aunque no se puedan establecer los permisos

            # Verificar la instalación
            try:
                # Verificar node
                result = subprocess.run([node_binary, '--version'],
                                        check=True,
                                        capture_output=True,
                                        text=True)
                self.logger.info(f"Node.js verificado correctamente: {result.stdout.strip()}")

                # Verificar npm usando el wrapper
                result = subprocess.run(['sh', str(npm_wrapper), '--version'],
                                        check=True,
                                        capture_output=True,
                                        text=True)
                self.logger.info(f"npm verificado correctamente: {result.stdout.strip()}")

                # Guardar las rutas
                os.environ['NODE_BINARY'] = node_binary
                os.environ['NPM_BINARY'] = str(npm_wrapper)
                os.environ['NODE_PATH'] = f"{extracted_dir}/lib/node_modules"
                os.environ['PATH'] = f"{bin_dir}:{os.environ.get('PATH', '')}"

                self.logger.info("Node.js instalado y configurado correctamente")
                return True
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error verificando la instalación: {str(e)}")
                if e.stdout:
                    self.logger.error(f"Stdout: {e.stdout}")
                if e.stderr:
                    self.logger.error(f"Stderr: {e.stderr}")
                return False

        except Exception as e:
            self.logger.error(f"Error instalando Node.js: {str(e)}")
            return False