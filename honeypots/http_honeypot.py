import socket
import threading
import logging
from datetime import datetime
import sys
import os
import re
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
        logging.FileHandler(os.path.join(LOG_DIR, 'http_honeypot.log')),
        logging.StreamHandler()
    ]
)

class HTTPHoneypot:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.running = False
        self.logger = logging.getLogger('HTTPHoneypot')
        
    def start(self):
        self.running = True
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        
        self.logger.info(f" HTTP Honeypot escutando em {self.host}:{self.port}")
        
        while self.running:
            try:
                client, address = server.accept()
                self.logger.warning(f" Conexão HTTP de {address[0]}:{address[1]}")
                
                client_handler = threading.Thread(
                    target=self.handle_connection,
                    args=(client, address)
                )
                client_handler.daemon = True
                client_handler.start()
                
            except Exception as e:
                if self.running:
                    self.logger.error(f"Erro no servidor: {e}")
    
    def handle_connection(self, client, address):
        client.settimeout(5)
        
        try:
            # Receber request HTTP completo
            request_data = b''
            while True:
                try:
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    request_data += chunk
                    if b'\r\n\r\n' in request_data:
                        break
                    if len(request_data) > 8192:  # Limite de 8KB
                        break
                except socket.timeout:
                    break
            
            if not request_data:
                self.logger.info(f"Conexão sem dados de {address[0]}")
                return
            
            # Parse do request
            request_text = request_data.decode('utf-8', errors='ignore')
            lines = request_text.split('\r\n')
            
            if not lines or not lines[0]:
                return
            
            # Parse primeira linha
            parts = lines[0].split(' ')
            if len(parts) < 2:
                return
            
            method = parts[0]
            path = parts[1]
            
            self.logger.info(f" Request: {method} {path} de {address[0]}")
            
            # SEMPRE registrar a tentativa
            self.log_attempt(address, method, path, request_text)
            
            # Detectar e marcar ataques específicos
            self.detect_and_log_attack(address, method, path, request_text)
            
            # Responder
            self.send_response(client, path)
            
        except Exception as e:
            self.logger.error(f"Erro na conexão HTTP: {e}")
            self.logger.error(traceback.format_exc())
        finally:
            try:
                client.close()
            except:
                pass
    
    def log_attempt(self, address, method, path, request_text):
        """Registrar TODA tentativa de conexão"""
        try:
            location = geo_locator.get_location(address[0])
            
            attempt = AttackAttempt(
                timestamp=datetime.utcnow(),
                source_ip=address[0],
                source_port=address[1],
                destination_port=self.port,
                protocol='HTTP',
                username=None,
                password=None,
                payload=f"{method} {path}",
                honeypot_type='http',
                country=location.get('country'),
                city=location.get('city'),
                latitude=location.get('latitude'),
                longitude=location.get('longitude'),
                risk_score=0.0
            )
            
            db = SessionLocal()
            db.add(attempt)
            db.commit()
            
            self.logger.info(f" Tentativa HTTP salva no banco (ID: {attempt.id})")
            
        except Exception as e:
            self.logger.error(f" Erro ao salvar tentativa HTTP: {e}")
            self.logger.error(traceback.format_exc())
        finally:
            try:
                db.close()
            except:
                pass
    
    def detect_and_log_attack(self, address, method, path, request_text):
        """Detectar e marcar ataques específicos"""
        patterns = {
            'SQL Injection': [
                r"(?:'|%27).*(?:OR|UNION|SELECT|INSERT|DELETE|DROP)",
                r"UNION.*SELECT",
                r"OR.*1=1",
            ],
            'XSS': [
                r"<script>",
                r"javascript:",
                r"onerror=",
                r"onload=",
            ],
            'Path Traversal': [
                r"\.\./",
                r"\.\.\\\\",
                r"%2e%2e",
            ],
            'Command Injection': [
                r";.*(?:ls|cat|rm|wget|curl|bash|sh)",
                r"cmd=",
                r"exec=",
                r"system\(",
            ],
            'File Access': [
                r"\.env",
                r"config\.php",
                r"wp-config",
                r"\.bak",
                r"\.backup",
            ]
        }
        
        detected_attacks = []
        
        for attack_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, request_text, re.IGNORECASE):
                    detected_attacks.append(attack_type)
                    break
        
        if detected_attacks:
            self.logger.warning(f" Ataques detectados de {address[0]}: {', '.join(detected_attacks)}")
            
            # Atualizar o último registro com o tipo de ataque
            try:
                db = SessionLocal()
                last_attempt = db.query(AttackAttempt)\
                    .filter(AttackAttempt.source_ip == address[0])\
                    .order_by(AttackAttempt.id.desc())\
                    .first()
                
                if last_attempt:
                    last_attempt.payload = f"{method} {path} - {', '.join(detected_attacks)}"
                    last_attempt.risk_score = 50.0 if len(detected_attacks) > 1 else 30.0
                    db.commit()
                    self.logger.info(f" Ataque atualizado no banco (ID: {last_attempt.id})")
            except Exception as e:
                self.logger.error(f" Erro ao atualizar ataque: {e}")
            finally:
                try:
                    db.close()
                except:
                    pass
    
    def send_response(self, client, path):
        """Enviar resposta HTTP falsa"""
        if '/admin' in path or 'wp-admin' in path:
            content = '<h1>Admin Login</h1><form method="POST"><input type="text" name="username"><input type="password" name="password"><input type="submit"></form>'
            status = "200 OK"
        elif 'phpmyadmin' in path:
            content = '<h1>phpMyAdmin</h1><p>Welcome to phpMyAdmin</p>'
            status = "200 OK"
        elif '.env' in path:
            content = 'DB_PASSWORD=fake_password_123\nAPI_KEY=fake_key_456'
            status = "200 OK"
        elif 'shell' in path or 'cmd' in path:
            content = '<html><body><h1>Command executed</h1><pre>root:x:0:0:root:/root:/bin/bash</pre></body></html>'
            status = "200 OK"
        else:
            content = '<h1>404 Not Found</h1>'
            status = "404 Not Found"
        
        response = f"""HTTP/1.1 {status}
Server: Apache/2.4.29 (Ubuntu)
Content-Type: text/html; charset=UTF-8
Content-Length: {len(content)}
Connection: close

{content}"""
        
        try:
            client.send(response.encode())
        except:
            pass

if __name__ == "__main__":
    honeypot = HTTPHoneypot()
    try:
        honeypot.start()
    except KeyboardInterrupt:
        print("\n🛑 Honeypot HTTP encerrado")
        honeypot.running = False
