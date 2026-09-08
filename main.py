import uvicorn
import threading
import sys
import os
import time

# Adicionar caminho do projeto ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import config
from honeypots.ssh_honeypot import SSHHoneypot
from honeypots.http_honeypot import HTTPHoneypot

def start_ssh_honeypot():
    honeypot = SSHHoneypot(port=config.HONEYPOT_PORT)
    honeypot.start()

def start_http_honeypot():
    honeypot = HTTPHoneypot(port=8080)
    honeypot.start()

def start_api():
    uvicorn.run(
        "core.api:app",
        host="0.0.0.0",
        port=config.API_PORT,
        reload=False
    )

def start_dashboard():
    uvicorn.run(
        "dashboard.server:app",
        host="0.0.0.0",
        port=8888,
        reload=False
    )

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════╗
    ║     🛡️  SENTINEL - Starting...        ║
    ╚═══════════════════════════════════════╝
    """)
    
    print(f"📁 Diretório do projeto: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"🔒 SSH Honeypot na porta {config.HONEYPOT_PORT}")
    print(f"🌐 HTTP Honeypot na porta 8080")
    print(f"📡 API na porta {config.API_PORT}")
    print(f"🖥️  Dashboard na porta 8888")
    print("")
    
    # Iniciar honeypots em threads separadas
    ssh_thread = threading.Thread(target=start_ssh_honeypot, daemon=True)
    ssh_thread.start()
    print("✅ SSH Honeypot iniciado")
    
    http_thread = threading.Thread(target=start_http_honeypot, daemon=True)
    http_thread.start()
    print("✅ HTTP Honeypot iniciado")
    
    # Iniciar dashboard em thread separada
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()
    print("✅ Dashboard iniciado")
    
    # Pequena pausa para os serviços iniciarem
    time.sleep(2)
    
    # Iniciar API (thread principal)
    try:
        print("✅ API iniciada")
        start_api()
    except KeyboardInterrupt:
        print("\n🛑 Sentinel encerrado")
        sys.exit(0)
