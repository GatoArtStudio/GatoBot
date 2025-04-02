import os
import yaml
import socket
import threading
import select

from sqlalchemy.orm import Session

from core.logging import Logger
from database.connection import Database
from config.config import PORT_SERVER_PROXY
from models.ip import Ip

# Instancia el debug
logger = Logger().get_logger()

class ServerProxy:

    session_database: Session

    def __init__(self):
        self.host = '0.0.0.0'
        self.port = int(PORT_SERVER_PROXY)
        self.buffer_size = 4096
        self.server_socket = None
        self.session_database = Database().get_session()
        self.is_running = threading.Event()
        self.list_ip = None
        self.load_whitelist()

    def handle_client(self, client_socket: socket.socket, client_address: tuple):
        client_ip, client_port = client_address

        # Verificamos si la ip esta permitida
        if not self.is_ip_whitelist(client_ip):
            logger.warning(f'IP no permitida: {client_ip}')
            client_socket.sendall(b'HTTP/1.1 403 Forbidden\r\n\r\nAcceso denegado')
            client_socket.close()
            return


        request = client_socket.recv(self.buffer_size)
        logger.info(f"Request: {request}")
        first_line = request.split(b'\n')[0]
        method, url, _ = first_line.split(b' ')
        
        if method == b'CONNECT':  # Manejo de HTTPS
            dest_host, dest_port = url.split(b':')
            dest_port = int(dest_port)
            
            try:
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((dest_host.decode(), dest_port))
                client_socket.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')
                
                sockets = [client_socket, remote_socket]
                while True:
                    ready_sockets, _, _ = select.select(sockets, [], [])
                    for sock in ready_sockets:
                        data = sock.recv(self.buffer_size)
                        if not data:
                            break
                        if sock is client_socket:
                            remote_socket.sendall(data)
                        else:
                            client_socket.sendall(data)
            except Exception as e:
                logger.error(f"Error en la conexión HTTPS: {e}")
            finally:
                remote_socket.close()
                client_socket.close()
        else:  # Manejo de HTTP
            http_pos = url.find(b'://')
            temp = url[(http_pos+3):] if http_pos != -1 else url
            port_pos = temp.find(b':')
            server_pos = temp.find(b'/')
            if server_pos == -1:
                server_pos = len(temp)
            server = temp[:port_pos] if port_pos != -1 else temp[:server_pos]
            port = int(temp[(port_pos+1):server_pos]) if port_pos != -1 else 80
            
            try:
                remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote_socket.connect((server.decode(), port))
                
                # Agregar encabezados si no están presentes
                if b'User-Agent:' not in request:
                    request += b'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36\r\n'
                if b'Connection:' not in request:
                    request += b'Connection: close\r\n'
                request += b'\r\n'
                
                remote_socket.sendall(request)
                
                while True:
                    ready_sockets, _, _ = select.select([remote_socket], [], [], 3)
                    if ready_sockets:
                        response = remote_socket.recv(self.buffer_size)
                        if len(response):
                            client_socket.send(response)
                        else:
                            break
                    else:
                        break
            except Exception as e:
                logger.error(f"Error en la conexión HTTP: {e}")
            finally:
                remote_socket.close()
                client_socket.close()
    
    def load_whitelist(self):
        '''
        Cargamos la whitelist
        '''

        # Extraemos las ips de la base de datos
        ips = self.session_database.query(Ip).all()

        # Extrae las IPs de la lista de objetos Ip
        self.list_ip = [ip.ip for ip in ips]
    
    def save_whitelist(self):
        '''
        Guardamos la whitelist
        '''
        # Eliminamos todas la IPs registradas en la base de datos
        self.session_database.query(Ip).delete()

        # Agregamos las nuevas IPs
        for ip in self.list_ip:
            new_ip = Ip(ip=ip)
            self.session_database.add(new_ip)

        # Guardamos los cambios
        self.session_database.commit()

    def add_ip_whitelist(self, ip):
        '''
        Agregamos una ip a la whitelist
        '''
        self.list_ip.append(ip)
        self.save_whitelist()
    
    def remove_ip_whitelist(self, ip):
        '''
        Removemos una ip de la whitelist
        '''
        self.list_ip.remove(ip)
        self.save_whitelist()
    
    def is_ip_whitelist(self, ip):
        '''
        Verificamos si una ip esta en la whitelist
        '''
        return ip in self.list_ip

    def start_proxy(self):
        '''
        Iniciamos el servidor proxy
        '''
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            logger.info(f'proxy escuchando en {self.host}:{self.port}')
            self.is_running.set()
        except Exception as e:
            logger.warning('Error al iniciar servidor proxy')
            logger.error(e)
            return

        while self.is_running.is_set():
            client_socket, client_address = self.server_socket.accept()
            logger.info(f"Conexion aceptada desde {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
    
    def stop_proxy(self):
        '''
        termina el servidor proxy
        '''
        self.is_running.clear()
        if self.server_socket:
            self.server_socket.close()
            logger.info('proxy detenido')