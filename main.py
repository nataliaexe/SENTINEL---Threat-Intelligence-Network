import uvicorn
import threading
import sys
import os
import time
import importlib.util

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import config
from honeypots.ssh_honeypot import SSHHoneypot
from honeypots.http_honeypot import HTTPHoneypot

PORT = int(os.getenv('PORT', 8000))

def start_ssh_honeypot():
    try:
        honeypot = SSHHoneypot(port=2222)
        honeypot.start()
    except Exception as e:
        print(f"SSH Honeypot error: {e}")

def start_http_honeypot():
    try:
        honeypot = HTTPHoneypot(port=8080)
        honeypot.start()
    except Exception as e:
        print(f"HTTP Honeypot error: {e}")

def start_server():
    from core.api import app as api_app
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    main_app = FastAPI(title="Sentinel", version="1.0.0")
    
    dashboard_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "dashboard", 
        "server.py"
    )
    
    spec = importlib.util.spec_from_file_location("dashboard_server", dashboard_path)
    dashboard_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dashboard_module)
    
    @main_app.get("/", response_class=HTMLResponse)
    async def landing():
        return dashboard_module.LANDING_PAGE
    
    @main_app.get("/dashboard", response_class=HTMLResponse)
    async def dashboard():
        return dashboard_module.DASHBOARD
    
    main_app.mount("/api", api_app)
    
    print(f"Dashboard disponivel em /")
    print(f"Dashboard disponivel em /dashboard")
    print(f"API disponivel em /api/*")
    
    uvicorn.run(main_app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    print("""
    ========================================
           SENTINEL - Starting...
    ========================================
    """)
    
    print(f"Servidor na porta {PORT}")
    print("SSH Honeypot na porta 2222 (interno)")
    print("HTTP Honeypot na porta 8080 (interno)")
    print("")
    
    ssh_thread = threading.Thread(target=start_ssh_honeypot, daemon=True)
    ssh_thread.start()
    print("SSH Honeypot iniciado")
    
    http_thread = threading.Thread(target=start_http_honeypot, daemon=True)
    http_thread.start()
    print("HTTP Honeypot iniciado")
    
    time.sleep(2)
    
    try:
        print(f"Servidor iniciado na porta {PORT}")
        start_server()
    except KeyboardInterrupt:
        print("\nSentinel encerrado")
        sys.exit(0)
