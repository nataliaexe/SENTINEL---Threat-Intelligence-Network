import uvicorn
import threading
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import config
from honeypots.ssh_honeypot import SSHHoneypot
from honeypots.http_honeypot import HTTPHoneypot

# Render usa a variável PORT
PORT = int(os.getenv('PORT', 8000))

def start_ssh_honeypot():
    try:
        honeypot = SSHHoneypot(port=2222)
        honeypot.start()
    except Exception as e:
        print(f" SSH Honeypot error: {e}")

def start_http_honeypot():
    try:
        honeypot = HTTPHoneypot(port=8080)
        honeypot.start()
    except Exception as e:
        print(f" HTTP Honeypot error: {e}")

def start_api():
    uvicorn.run(
        "core.api:app",
        host="0.0.0.0",
        port=PORT,
        reload=False
    )

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║        SENTINEL - Starting...         ║
    ╚═══════════════════════════════════════╝
    """)
    
    print(f" API na porta {PORT}")
    print(" SSH Honeypot na porta 2222 (interno)")
    print(" HTTP Honeypot na porta 8080 (interno)")
    print("")
    
    # Iniciar honeypots em background
    ssh_thread = threading.Thread(target=start_ssh_honeypot, daemon=True)
    ssh_thread.start()
    print(" SSH Honeypot iniciado")
    
    http_thread = threading.Thread(target=start_http_honeypot, daemon=True)
    http_thread.start()
    print(" HTTP Honeypot iniciado")
    
    # Pequena pausa
    time.sleep(2)
    
    # Iniciar API (thread principal)
    try:
        print(f" API iniciada na porta {PORT}")
        start_api()
    except KeyboardInterrupt:
        print("\n Sentinel encerrado")
        sys.exit(0)
