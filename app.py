import uvicorn
import threading
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import config
from honeypots.ssh_honeypot import SSHHoneypot
from honeypots.http_honeypot import HTTPHoneypot
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from core.api import app as api_app

PORT = int(os.getenv('PORT', 8000))

# ============ LANDING PAGE (TELA 1) ============
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>SENTINEL - Threat Intelligence Network</title>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #111111;
            --silver-dark: #1a1a1a;
            --silver-medium: #2a2a2a;
            --silver-light: #4a4a4a;
            --silver-bright: #8a8a8a;
            --silver-ice: #c0c0c0;
            --text-primary: #d0d0d0;
            --text-secondary: #808080;
            --border: #2a2a2a;
            --section-spacing: 100px;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            position: relative;
            overflow-x: hidden;
        }
        #ascii-ripple {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
            opacity: 0.15;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 40px;
            position: relative;
            z-index: 2;
        }
        .section { margin-bottom: var(--section-spacing); }
        .hero {
            text-align: center;
            padding: 120px 20px;
            margin-bottom: 160px;
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .hero h1 {
            font-size: 5em;
            font-weight: 300;
            letter-spacing: 0.4em;
            color: var(--silver-ice);
            margin-bottom: 30px;
        }
        .hero .tagline {
            font-size: 1.4em;
            color: var(--text-secondary);
            letter-spacing: 0.3em;
            margin-bottom: 60px;
            text-transform: uppercase;
        }
        .hero .description {
            max-width: 800px;
            font-size: 1em;
            color: var(--text-secondary);
            line-height: 2.2;
        }
        .cta-button {
            display: inline-block;
            padding: 20px 50px;
            margin-top: 80px;
            background: var(--bg-secondary);
            border: 1px solid var(--silver-light);
            color: var(--silver-ice);
            text-decoration: none;
            font-size: 1em;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            transition: all 0.4s;
        }
        .cta-button:hover {
            background: var(--silver-dark);
            border-color: var(--silver-bright);
            box-shadow: 0 0 40px rgba(192, 192, 192, 0.15);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2px;
            background: var(--border);
            border: 1px solid var(--border);
        }
        .feature {
            background: var(--bg-secondary);
            padding: 50px 40px;
            transition: all 0.4s;
        }
        .feature:hover {
            background: var(--silver-dark);
            transform: translateY(-5px);
        }
        .feature-icon { font-size: 3em; margin-bottom: 25px; opacity: 0.7; }
        .feature h3 {
            font-size: 1.1em;
            font-weight: 300;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--silver-ice);
            margin-bottom: 20px;
        }
        .feature p { font-size: 0.9em; color: var(--text-secondary); line-height: 2; }
        .section-title {
            text-align: center;
            font-size: 2em;
            font-weight: 300;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--silver-ice);
            margin-bottom: 80px;
        }
        .steps {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 40px;
        }
        .step {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            padding: 50px 30px;
            text-align: center;
            transition: all 0.4s;
        }
        .step:hover { background: var(--silver-dark); transform: translateY(-5px); }
        .step-number { font-size: 3em; color: var(--silver-bright); opacity: 0.3; margin-bottom: 25px; }
        .step h4 {
            font-size: 1em;
            font-weight: 300;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--silver-ice);
            margin-bottom: 20px;
        }
        .step p { font-size: 0.85em; color: var(--text-secondary); line-height: 1.8; }
        .faq-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }
        .faq-question {
            padding: 30px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 1em;
            color: var(--silver-ice);
        }
        .faq-answer {
            padding: 0 30px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s, padding 0.4s;
            font-size: 0.9em;
            color: var(--text-secondary);
            line-height: 2;
        }
        .faq-item.active .faq-answer { max-height: 300px; padding: 30px; }
        .faq-toggle { font-size: 2em; color: var(--silver-bright); transition: transform 0.3s; }
        .faq-item.active .faq-toggle { transform: rotate(45deg); }
        .contact-section {
            text-align: center;
            padding: 100px 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
        }
        .contact-links {
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 60px;
        }
        .contact-link {
            display: inline-flex;
            align-items: center;
            gap: 15px;
            padding: 20px 30px;
            background: var(--bg-primary);
            border: 1px solid var(--silver-medium);
            color: var(--silver-ice);
            text-decoration: none;
            font-size: 0.9em;
            letter-spacing: 0.1em;
            transition: all 0.4s;
            text-transform: uppercase;
        }
        .contact-link:hover {
            background: var(--silver-dark);
            border-color: var(--silver-bright);
            transform: translateY(-3px);
        }
        .footer {
            text-align: center;
            padding: 60px;
            margin-top: 100px;
            border-top: 1px solid var(--border);
            font-size: 0.8em;
            color: var(--text-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <canvas id="ascii-ripple"></canvas>
    <div class="container">
        <div class="hero">
            <h1>SENTINEL</h1>
            <div class="tagline">Threat Intelligence Network</div>
            <div class="description">
                Um sistema avançado de honeypots que detecta, analisa e monitora 
                tentativas de ataques cibernéticos em tempo real.
            </div>
            <a href="/dashboard" class="cta-button">Acessar Dashboard</a>
        </div>
        
        <div class="section">
            <h2 class="section-title">Funcionalidades</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">[SSH]</div>
                    <h3>Honeypot SSH</h3>
                    <p>Simula servidor SSH vulnerável e captura tentativas de login.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">[HTTP]</div>
                    <h3>Honeypot HTTP</h3>
                    <p>Detecta SQL Injection, XSS e outros ataques web.</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">[LIVE]</div>
                    <h3>Análise em Tempo Real</h3>
                    <p>Dashboard ao vivo com estatísticas e terminal integrado.</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">Como Funciona</h2>
            <div class="steps">
                <div class="step">
                    <div class="step-number">01</div>
                    <h4>Atrair</h4>
                    <p>Honeypots simulam serviços vulneráveis para atrair atacantes.</p>
                </div>
                <div class="step">
                    <div class="step-number">02</div>
                    <h4>Capturar</h4>
                    <p>Cada ataque é registrado com IP, credenciais e payloads.</p>
                </div>
                <div class="step">
                    <div class="step-number">03</div>
                    <h4>Analisar</h4>
                    <p>O sistema processa dados em tempo real e classifica riscos.</p>
                </div>
                <div class="step">
                    <div class="step-number">04</div>
                    <h4>Aprender</h4>
                    <p>Inteligência coletada ajuda a fortalecer defesas.</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            SENTINEL v1.0 // Open Source
        </div>
    </div>
    <script>
        const canvas = document.getElementById('ascii-ripple');
        const ctx = canvas.getContext('2d');
        const chars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@'];
        const fontSize = 10;
        let cols, rows, grid = [], ripples = [];
        function init() {
            canvas.width = innerWidth; canvas.height = innerHeight;
            cols = Math.floor(canvas.width / fontSize);
            rows = Math.floor(canvas.height / fontSize);
            grid = [];
            for (let y = 0; y < rows; y++) {
                grid[y] = [];
                for (let x = 0; x < cols; x++) grid[y][x] = 0;
            }
        }
        function ripple(x, y) {
            ripples.push({x, y, r: 0, max: 100, life: 1});
        }
        function animate() {
            ctx.fillStyle = '#0a0a0a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.font = fontSize + 'px monospace';
            ctx.textAlign = 'center';
            for (let y = 0; y < rows; y++)
                for (let x = 0; x < cols; x++) grid[y][x] *= 0.95;
            for (let i = ripples.length - 1; i >= 0; i--) {
                const rp = ripples[i];
                rp.r += 2; rp.life -= 0.02;
                if (rp.life <= 0 || rp.r > rp.max) ripples.splice(i, 1);
                const cx = rp.x / fontSize, cy = rp.y / fontSize, rad = rp.r / fontSize;
                for (let y = 0; y < rows; y++)
                    for (let x = 0; x < cols; x++) {
                        const d = Math.sqrt((x-cx)**2 + (y-cy)**2);
                        if (Math.abs(d - rad) < 1)
                            grid[y][x] = Math.max(grid[y][x], rp.life);
                    }
            }
            for (let y = 0; y < rows; y++)
                for (let x = 0; x < cols; x++)
                    if (grid[y][x] > 0.01) {
                        const ci = Math.floor(grid[y][x] * 9);
                        const b = Math.floor(128 + grid[y][x] * 127);
                        ctx.fillStyle = `rgb(${b},${b},${b})`;
                        ctx.fillText(chars[ci], x*fontSize+5, y*fontSize+5);
                    }
            requestAnimationFrame(animate);
        }
        addEventListener('mousemove', e => { if (Math.random() < 0.3) ripple(e.clientX, e.clientY); });
        addEventListener('click', e => ripple(e.clientX, e.clientY));
        setInterval(() => { if (Math.random() < 0.5) ripple(Math.random()*innerWidth, Math.random()*innerHeight); }, 3000);
        init(); animate();
    </script>
</body>
</html>
"""

# ============ DASHBOARD (TELA 2) ============
DASHBOARD = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>SENTINEL - Dashboard</title>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg-primary: #0a0a0a;
            --bg-secondary: #111111;
            --silver-dark: #1a1a1a;
            --silver-medium: #2a2a2a;
            --silver-light: #4a4a4a;
            --silver-bright: #8a8a8a;
            --silver-ice: #c0c0c0;
            --text-primary: #d0d0d0;
            --text-secondary: #808080;
            --border: #2a2a2a;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 40px; }
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            margin-bottom: 40px;
        }
        .nav-brand {
            font-size: 1.5em;
            letter-spacing: 0.2em;
            color: var(--silver-ice);
            text-decoration: none;
        }
        .nav-links { display: flex; gap: 30px; }
        .nav-link {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.75em;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .nav-link:hover { color: var(--silver-ice); }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1px;
            background: var(--border);
            border: 1px solid var(--border);
            margin-bottom: 40px;
        }
        .stat-card {
            background: var(--bg-secondary);
            padding: 30px;
            text-align: center;
        }
        .stat-value {
            font-size: 2.5em;
            color: var(--silver-ice);
            margin: 15px 0;
        }
        .stat-label {
            font-size: 0.7em;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        @media (max-width: 1024px) { .main-content { grid-template-columns: 1fr; } }
        .terminal-container, .attacks-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            height: 500px;
            display: flex;
            flex-direction: column;
        }
        .terminal-header {
            padding: 15px 20px;
            border-bottom: 1px solid var(--border);
            background: var(--silver-dark);
        }
        .terminal-output, .attacks-list {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            font-size: 0.8em;
        }
        .attack-item {
            padding: 15px;
            border-bottom: 1px solid var(--border);
        }
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border: 1px solid var(--silver-medium);
            font-size: 0.7em;
            text-transform: uppercase;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="nav">
            <a href="/" class="nav-brand">SENTINEL</a>
            <div class="nav-links">
                <a href="/" class="nav-link">Voltar</a>
            </div>
        </div>
        
        <div class="stats-grid" id="stats">
            <div class="stat-card">
                <div class="stat-value">...</div>
                <div class="stat-label">Loading</div>
            </div>
        </div>
        
        <div class="main-content">
            <div class="terminal-container">
                <div class="terminal-header">LIVE TERMINAL</div>
                <div class="terminal-output" id="terminal">
                    <p>System initialized...</p>
                </div>
            </div>
            
            <div class="attacks-container">
                <div class="terminal-header">RECENT ATTACKS</div>
                <div class="attacks-list" id="attacks">
                    <p>Loading...</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        async function loadStats() {
            const res = await fetch('/api/stats');
            const data = await res.json();
            document.getElementById('stats').innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${data.total_attacks}</div>
                    <div class="stat-label">Total Attacks</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.unique_ips}</div>
                    <div class="stat-label">Unique IPs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${data.recent_attacks_5min}</div>
                    <div class="stat-label">Last 5 min</div>
                </div>
            `;
        }
        async function loadAttacks() {
            const res = await fetch('/api/attacks?limit=20');
            const attacks = await res.json();
            if (!attacks || attacks.length === 0) {
                document.getElementById('attacks').innerHTML = '<p>No attacks yet</p>';
                return;
            }
            document.getElementById('attacks').innerHTML = attacks.map(a => `
                <div class="attack-item">
                    <span class="badge">${a.honeypot_type}</span>
                    ${a.source_ip} | ${new Date(a.timestamp).toLocaleTimeString()}
                </div>
            `).join('');
        }
        loadStats();
        loadAttacks();
        setInterval(loadStats, 5000);
        setInterval(loadAttacks, 5000);
    </script>
</body>
</html>
"""

app = FastAPI(title="Sentinel")

@app.get("/", response_class=HTMLResponse)
async def home():
    return LANDING_PAGE

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return DASHBOARD

# Copiar rotas da API
for route in api_app.routes:
    app.routes.append(route)

def start_ssh():
    try:
        SSHHoneypot(port=2222).start()
    except Exception as e:
        print(f"SSH: {e}")

def start_http():
    try:
        HTTPHoneypot(port=8080).start()
    except Exception as e:
        print(f"HTTP: {e}")

if __name__ == "__main__":
    print("SENTINEL starting...")
    threading.Thread(target=start_ssh, daemon=True).start()
    threading.Thread(target=start_http, daemon=True).start()
    time.sleep(2)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
