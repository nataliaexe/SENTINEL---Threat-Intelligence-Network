import socket
import threading
import logging
from datetime import datetime
import sys
import os
import time
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import AttackAttempt, SessionLocal
from utils.geo_locator import geo_locator

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'ssh_honeypot.log')),
        logging.StreamHandler()
    ]
)

class SSHHoneypot:
    def __init__(self, host='0.0.0.0', port=2222):
        self.host = host
        self.port = port
        self.running = False
        self.logger = logging.getLogger('SSHHoneypot')
        self.total_connections = 0
        
    def start(self):
        self.running = True
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        self.logger.info(f" SSH Honeypot escutando em {self.host}:{self.port}")
        
        while self.running:
            try:
                client, address = server.accept()
                self.total_connections += 1
                
                location = geo_locator.get_location(address[0])
                location_str = f"{location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}"
                
                self.logger.warning(f" Conexão #{self.total_connections} de {address[0]}:{address[1]} [{location_str}]")
                
                client_handler = threading.Thread(
                    target=self.handle_connection,
                    args=(client, address, location)
                )
                client_handler.daemon = True
                client_handler.start()
                
            except Exception as e:
                if self.running:
                    self.logger.error(f"Erro no servidor: {e}")
    
    def handle_connection(self, client, address, location=None):
        client.settimeout(10)
        
        try:
            # Enviar banner SSH
            client.send(b"SSH-2.0-OpenSSH_7.9p1 Ubuntu-10ubuntu2.7\r\n")
            
            # Aguardar resposta
            try:
                data = client.recv(1024)
                if not data:
                    return
            except socket.timeout:
                return
            
            time.sleep(0.5)
            
            # Enviar prompt
            client.send(b"login as: ")
            
            # Receber username
            try:
                username = client.recv(1024).decode('utf-8', errors='ignore').strip()
                if not username:
                    return
                self.logger.info(f"👤 Username: {username}")
            except socket.timeout:
                return
            
            # Enviar prompt de senha
            client.send(b"password: ")
            
            # Receber senha
            try:
                password = client.recv(1024).decode('utf-8', errors='ignore').strip()
                if not password:
                    return
                self.logger.warning(f"🔑 Senha capturada: {password}")
            except socket.timeout:
                return
            
            # SALVAR no banco de dados
            self.save_attempt(address, username, password, location)
            
            # Responder
            client.send(b"\r\nAccess denied\r\n")
            time.sleep(0.5)
            client.send(b"\r\nConnection closed by remote host.\r\n")
            
        except Exception as e:
            if "Broken pipe" not in str(e):
                self.logger.error(f"Erro na conexão: {e}")
        finally:
            try:
                client.close()
            except:
                pass
    
    def save_attempt(self, address, username, password, location=None):
        """Salvar tentativa no banco de dados"""
        try:
            attempt = AttackAttempt(
                timestamp=datetime.utcnow(),
                source_ip=address[0],
                source_port=address[1],
                destination_port=self.port,
                protocol='SSH',
                username=username,
                password=password,
                payload=f"SSH login attempt: {username}",
                honeypot_type='ssh',
                country=location.get('country') if location else None,
                city=location.get('city') if location else None,
                latitude=location.get('latitude') if location else None,
                longitude=location.get('longitude') if location else None,
                risk_score=30.0 if username == 'root' else 10.0
            )
            
            db = SessionLocal()
            db.add(attempt)
            db.commit()
            
            self.logger.info(f" Tentativa SSH salva no banco (ID: {attempt.id})")
            
        except Exception as e:
            self.logger.error(f" Erro ao salvar tentativa SSH: {e}")
            self.logger.error(traceback.format_exc())
        finally:
            try:
                db.close()
            except:
                pass

if __name__ == "__main__":
    honeypot = SSHHoneypot()
    try:
        honeypot.start()
    except KeyboardInterrupt:
        print("\n🛑 Honeypot encerrado")
        honeypot.running = False
