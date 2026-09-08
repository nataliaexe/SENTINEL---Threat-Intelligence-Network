from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="Sentinel Dashboard")

# ============= LANDING PAGE =============
LANDING_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>SENTINEL - Threat Intelligence Network</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            --accent: #c0c0c0;
            --section-spacing: 120px;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'SF Mono', 'Courier New', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            position: relative;
            overflow-x: hidden;
            cursor: crosshair;
        }
        
        /* ASCII Ripple Canvas */
        #ascii-ripple {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            opacity: 0.15;
        }
        
        /* Reflexo de água sutil */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                180deg,
                transparent 0%,
                rgba(192, 192, 192, 0.02) 30%,
                transparent 50%,
                rgba(192, 192, 192, 0.02) 70%,
                transparent 100%
            );
            animation: waterReflection 10s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes waterReflection {
            0%, 100% { transform: translateY(-2%); opacity: 0.3; }
            50% { transform: translateY(2%); opacity: 0.6; }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 60px 40px;
            position: relative;
            z-index: 2;
        }
        
        /* Seções com MUITO espaço */
        .section {
            margin-bottom: var(--section-spacing);
            position: relative;
        }
        
        /* Hero Section */
        .hero {
            text-align: center;
            padding: 120px 20px;
            margin-bottom: 160px;
            position: relative;
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
            animation: fadeInDown 1s ease-out;
            text-shadow: 0 0 30px rgba(192, 192, 192, 0.2);
        }
        
        .hero .tagline {
            font-size: 1.4em;
            color: var(--text-secondary);
            letter-spacing: 0.3em;
            margin-bottom: 60px;
            animation: fadeIn 1.5s ease-out;
            text-transform: uppercase;
        }
        
        .hero .description {
            max-width: 800px;
            margin: 0 auto;
            font-size: 1em;
            color: var(--text-secondary);
            line-height: 2.2;
            animation: fadeIn 2s ease-out;
            padding: 0 20px;
        }
        
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-40px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* CTA Button */
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
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .cta-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(192, 192, 192, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .cta-button:hover::before {
            left: 100%;
        }
        
        .cta-button:hover {
            background: var(--silver-dark);
            border-color: var(--silver-bright);
            box-shadow: 0 0 40px rgba(192, 192, 192, 0.15);
            transform: translateY(-2px);
        }
        
        /* Features Grid */
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
            position: relative;
        }
        
        .feature:hover {
            background: var(--silver-dark);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        
        .feature-icon {
            font-size: 3em;
            margin-bottom: 25px;
            color: var(--silver-bright);
            opacity: 0.7;
        }
        
        .feature h3 {
            font-size: 1.1em;
            font-weight: 300;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--silver-ice);
            margin-bottom: 20px;
        }
        
        .feature p {
            font-size: 0.9em;
            color: var(--text-secondary);
            line-height: 2;
        }
        
        /* How it works */
        .section-title {
            text-align: center;
            font-size: 2em;
            font-weight: 300;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: var(--silver-ice);
            margin-bottom: 80px;
            position: relative;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--silver-bright), transparent);
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
            position: relative;
            transition: all 0.4s;
        }
        
        .step:hover {
            background: var(--silver-dark);
            transform: translateY(-5px);
        }
        
        .step-number {
            font-size: 3em;
            color: var(--silver-bright);
            margin-bottom: 25px;
            opacity: 0.3;
            font-weight: 100;
        }
        
        .step h4 {
            font-size: 1em;
            font-weight: 300;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--silver-ice);
            margin-bottom: 20px;
        }
        
        .step p {
            font-size: 0.85em;
            color: var(--text-secondary);
            line-height: 1.8;
        }
        
        /* FAQ */
        .faq-item {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        
        .faq-item:hover {
            border-color: var(--silver-light);
        }
        
        .faq-question {
            padding: 30px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 1em;
            letter-spacing: 0.05em;
            color: var(--silver-ice);
            transition: background 0.3s;
        }
        
        .faq-question:hover {
            background: var(--silver-dark);
        }
        
        .faq-answer {
            padding: 0 30px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-out, padding 0.4s;
            font-size: 0.9em;
            color: var(--text-secondary);
            line-height: 2;
        }
        
        .faq-item.active .faq-answer {
            max-height: 300px;
            padding: 30px;
        }
        
        .faq-toggle {
            font-size: 2em;
            color: var(--silver-bright);
            transition: transform 0.3s;
            font-weight: 100;
        }
        
        .faq-item.active .faq-toggle {
            transform: rotate(45deg);
        }
        
        /* Contact Section */
        .contact-section {
            text-align: center;
            padding: 100px 20px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            position: relative;
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
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }
        
        .contact-icon {
            font-size: 1.5em;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 60px 40px;
            margin-top: 120px;
            border-top: 1px solid var(--border);
            font-size: 0.8em;
            color: var(--text-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            position: relative;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        
        .footer-link {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.8em;
            letter-spacing: 0.1em;
            transition: color 0.3s;
            text-transform: uppercase;
        }
        
        .footer-link:hover {
            color: var(--silver-ice);
        }
        
        .footer-social {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .social-icon {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-secondary);
            border: 1px solid var(--silver-medium);
            color: var(--silver-ice);
            text-decoration: none;
            font-size: 1.2em;
            transition: all 0.3s;
        }
        
        .social-icon:hover {
            background: var(--silver-dark);
            border-color: var(--silver-bright);
            transform: translateY(-3px);
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            :root {
                --section-spacing: 80px;
            }
            
            .container {
                padding: 30px 20px;
            }
            
            .hero {
                padding: 60px 20px;
                min-height: 60vh;
            }
            
            .hero h1 {
                font-size: 3em;
                letter-spacing: 0.2em;
            }
            
            .features {
                grid-template-columns: 1fr;
            }
            
            .steps {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .contact-links {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <!-- ASCII Ripple Canvas -->
    <canvas id="ascii-ripple"></canvas>
    
    <div class="container">
        <!-- Hero -->
        <div class="hero">
            <h1>SENTINEL</h1>
            <div class="tagline">Threat Intelligence Network</div>
            <div class="description">
                Um sistema avançado de honeypots que detecta, analisa e monitora 
                tentativas de ataques cibernéticos em tempo real. O Sentinel cria 
                armadilhas digitais que simulam serviços vulneráveis para atrair 
                atacantes e coletar inteligência sobre suas técnicas.
            </div>
            <a href="/dashboard" class="cta-button">Acessar Dashboard →</a>
        </div>
        
        <!-- Features -->
        <div class="section">
            <h2 class="section-title">Funcionalidades</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon"></div>
                    <h3>Honeypot SSH</h3>
                    <p>Simula um servidor SSH vulnerável que atrai atacantes tentando 
                    adivinhar credenciais. Captura usuários, senhas e IPs de origem 
                    com geolocalização em tempo real.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon"></div>
                    <h3>Honeypot HTTP</h3>
                    <p>Finge ser um servidor web com vulnerabilidades conhecidas. 
                    Detecta SQL Injection, XSS, Path Traversal e outros ataques web 
                    com classificação automática.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon"></div>
                    <h3>Análise em Tempo Real</h3>
                    <p>Dashboard ao vivo com estatísticas, terminal integrado e 
                    monitoramento contínuo de todas as atividades maliciosas.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon"></div>
                    <h3>Inteligência de Ameaças</h3>
                    <p>Coleta automática de dados sobre atacantes, incluindo 
                    geolocalização, padrões de ataque e credenciais mais usadas 
                    em tentativas de invasão.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon"></div>
                    <h3>Defesa Ativa</h3>
                    <p>Aprenda como atacantes operam e fortaleça suas defesas 
                    entendendo as técnicas mais comuns de invasão e exploração.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon"></div>
                    <h3>Exportação de Dados</h3>
                    <p>Exporte todos os dados coletados em JSON ou CSV para análise 
                    forense, documentação de incidentes e relatórios detalhados.</p>
                </div>
            </div>
        </div>
        
        <!-- How it works -->
        <div class="section">
            <h2 class="section-title">Como Funciona</h2>
            <div class="steps">
                <div class="step">
                    <div class="step-number">01</div>
                    <h4>Atrair</h4>
                    <p>Os honeypots simulam serviços vulneráveis e ficam expostos, 
                    atraindo atacantes que procuram alvos fáceis na internet.</p>
                </div>
                
                <div class="step">
                    <div class="step-number">02</div>
                    <h4>Capturar</h4>
                    <p>Cada tentativa de ataque é registrada com detalhes: IP, 
                    credenciais tentadas, payloads maliciosos e localização 
                    geográfica do atacante.</p>
                </div>
                
                <div class="step">
                    <div class="step-number">03</div>
                    <h4>Analisar</h4>
                    <p>O sistema processa os dados em tempo real, identificando 
                    padrões de ataque e classificando o nível de risco de cada 
                    tentativa de intrusão.</p>
                </div>
                
                <div class="step">
                    <div class="step-number">04</div>
                    <h4>Aprender</h4>
                    <p>Com a inteligência coletada, você entende como atacantes 
                    operam e pode fortalecer suas defesas de forma proativa.</p>
                </div>
            </div>
        </div>
        
        <!-- FAQ -->
        <div class="section">
            <h2 class="section-title">Perguntas Frequentes</h2>
            
            <div class="faq-item" onclick="toggleFAQ(this)">
                <div class="faq-question">
                    O que é um honeypot?
                    <span class="faq-toggle">+</span>
                </div>
                <div class="faq-answer">
                    Um honeypot é um sistema de segurança que simula ser um alvo 
                    vulnerável para atrair atacantes. Ele permite estudar as 
                    técnicas de ataque sem colocar sistemas reais em risco. É como 
                    uma armadilha digital para hackers.
                </div>
            </div>
            
            <div class="faq-item" onclick="toggleFAQ(this)">
                <div class="faq-question">
                    É legal usar honeypots?
                    <span class="faq-toggle">+</span>
                </div>
                <div class="faq-answer">
                    Sim, honeypots são legais quando usados em seus próprios 
                    servidores ou com autorização explícita. Eles são amplamente 
                    usados por empresas de segurança, universidades e pesquisadores 
                    em todo o mundo.
                </div>
            </div>
            
            <div class="faq-item" onclick="toggleFAQ(this)">
                <div class="faq-question">
                    Que tipos de ataques são detectados?
                    <span class="faq-toggle">+</span>
                </div>
                <div class="faq-answer">
                    O Sentinel detecta ataques SSH (força bruta, tentativas de 
                    login) e ataques web (SQL Injection, XSS, Path Traversal, 
                    Command Injection, acesso a arquivos sensíveis). Cada ataque 
                    é classificado e documentado.
                </div>
            </div>
            
            <div class="faq-item" onclick="toggleFAQ(this)">
                <div class="faq-question">
                    Como os dados são armazenados?
                    <span class="faq-toggle">+</span>
                </div>
                <div class="faq-answer">
                    Todos os ataques são armazenados em um banco de dados SQLite 
                    local. Você pode exportar os dados em JSON ou CSV a qualquer 
                    momento para análise externa, documentação ou compartilhamento 
                    com a comunidade de segurança.
                </div>
            </div>
            
            <div class="faq-item" onclick="toggleFAQ(this)">
                <div class="faq-question">
                    Posso usar em produção?
                    <span class="faq-toggle">+</span>
                </div>
                <div class="faq-answer">
                    Sim, mas requer configurações adicionais de segurança, como 
                    autenticação, firewalls e monitoramento. Para uso educacional 
                    e pesquisa, está pronto para uso imediato em ambiente controlado.
                </div>
            </div>
        </div>
        
        <!-- Contact -->
        <div class="section">
            <div class="contact-section">
                <h2 class="section-title">Contato & Contribuições</h2>
                <p style="color: var(--text-secondary); font-size: 1em; margin-bottom: 40px; letter-spacing: 0.05em;">
                    Tem sugestões, encontrou bugs ou quer contribuir com o projeto?
                </p>
                
                <div class="contact-links">
                    <a href="https://github.com/SEU_USUARIO_AQUI" target="_blank" class="contact-link">
                        <span class="contact-icon"></span>
                        GitHub
                    </a>
                    <a href="mailto:SEU_EMAIL_AQUI" class="contact-link">
                        <span class="contact-icon"></span>
                        Email
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-social">
                <a href="https://github.com/SEU_USUARIO_AQUI" target="_blank" class="social-icon" title="GitHub">GH</a>
                <a href="mailto:SEU_EMAIL_AQUI" class="social-icon" title="Email">@</a>
            </div>
            
            <div class="footer-links">
                <a href="/dashboard" class="footer-link">Dashboard</a>
                <a href="#features" class="footer-link">Funcionalidades</a>
                <a href="#faq" class="footer-link">FAQ</a>
                <a href="https://github.com/SEU_USUARIO_AQUI" target="_blank" class="footer-link">GitHub</a>
            </div>
            
            <p style="margin-bottom: 20px;">
                SENTINEL v1.0 // Open Source // Educational Project
            </p>
            
            <p style="opacity: 0.5;">
                Feito com 💜 para a comunidade de cybersecurity
            </p>
        </div>
    </div>
    
    <script>
        // ============= ASCII RIPPLE EFFECT =============
        const canvas = document.getElementById('ascii-ripple');
        const ctx = canvas.getContext('2d');
        
        // ASCII characters (from dark to bright)
        const asciiChars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@'];
        
        // Grid settings
        const fontSize = 10;
        let columns, rows;
        let grid = [];
        let ripples = [];
        
        // Mouse position
        let mouseX = -1000;
        let mouseY = -1000;
        
        function initGrid() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            
            columns = Math.floor(canvas.width / fontSize);
            rows = Math.floor(canvas.height / fontSize);
            
            grid = [];
            for (let y = 0; y < rows; y++) {
                grid[y] = [];
                for (let x = 0; x < columns; x++) {
                    grid[y][x] = 0; // All black initially
                }
            }
        }
        
        function createRipple(x, y, radius) {
            ripples.push({
                x: x,
                y: y,
                radius: radius,
                maxRadius: 100,
                speed: 2,
                life: 1.0,
                active: true
            });
        }
        
        function updateRipples() {
            for (let i = ripples.length - 1; i >= 0; i--) {
                const ripple = ripples[i];
                ripple.radius += ripple.speed;
                ripple.life -= 0.02;
                
                if (ripple.life <= 0 || ripple.radius > ripple.maxRadius) {
                    ripples.splice(i, 1);
                }
            }
        }
        
        function applyRipples() {
            // Reset grid
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < columns; x++) {
                    grid[y][x] *= 0.95; // Fade effect
                }
            }
            
            // Apply ripples
            for (const ripple of ripples) {
                const centerX = ripple.x / fontSize;
                const centerY = ripple.y / fontSize;
                const radius = ripple.radius / fontSize;
                
                for (let y = 0; y < rows; y++) {
                    for (let x = 0; x < columns; x++) {
                        const dx = x - centerX;
                        const dy = y - centerY;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        
                        if (Math.abs(distance - radius) < 1) {
                            const intensity = ripple.life * (1 - distance / ripple.maxRadius * fontSize);
                            grid[y][x] = Math.max(grid[y][x], intensity);
                        }
                    }
                }
            }
        }
        
        function render() {
            ctx.fillStyle = '#0a0a0a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.font = fontSize + 'px monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < columns; x++) {
                    const intensity = grid[y][x];
                    
                    if (intensity > 0.01) {
                        const charIndex = Math.floor(intensity * (asciiChars.length - 1));
                        const char = asciiChars[Math.min(charIndex, asciiChars.length - 1)];
                        
                        // Silver color with intensity
                        const brightness = Math.floor(128 + intensity * 127);
                        ctx.fillStyle = `rgb(${brightness}, ${brightness}, ${brightness})`;
                        
                        ctx.fillText(char, x * fontSize + fontSize / 2, y * fontSize + fontSize / 2);
                    }
                }
            }
        }
        
        function animate() {
            updateRipples();
            applyRipples();
            render();
            requestAnimationFrame(animate);
        }
        
        // Event listeners
        window.addEventListener('resize', initGrid);
        
        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            // Create ripple on mouse move (with throttle)
            if (Math.random() < 0.3) {
                createRipple(mouseX, mouseY, 0);
            }
        });
        
        window.addEventListener('click', (e) => {
            createRipple(e.clientX, e.clientY, 0);
        });
        
        // Auto ripples
        setInterval(() => {
            if (Math.random() < 0.5) {
                const x = Math.random() * canvas.width;
                const y = Math.random() * canvas.height;
                createRipple(x, y, 0);
            }
        }, 3000);
        
        // Initialize
        initGrid();
        animate();
        
        // ============= FAQ TOGGLE =============
        function toggleFAQ(element) {
            element.classList.toggle('active');
        }
    </script>
</body>
</html>
"""

# ============= DASHBOARD =============
DASHBOARD = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>SENTINEL - Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
            --section-spacing: 60px;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'SF Mono', 'Courier New', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            position: relative;
            cursor: crosshair;
        }
        
        /* ASCII Ripple Canvas */
        #ascii-ripple {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            opacity: 0.1;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 40px;
            position: relative;
            z-index: 2;
        }
        
        /* Navigation */
        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 30px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            margin-bottom: var(--section-spacing);
        }
        
        .nav-brand {
            font-size: 1.5em;
            letter-spacing: 0.2em;
            color: var(--silver-ice);
            text-decoration: none;
        }
        
        .nav-links {
            display: flex;
            gap: 30px;
            align-items: center;
        }
        
        .nav-link {
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.75em;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            transition: color 0.3s;
            cursor: pointer;
        }
        
        .nav-link:hover {
            color: var(--silver-ice);
        }
        
        /* Control Panel */
        .control-panel {
            display: flex;
            gap: 15px;
            margin-bottom: var(--section-spacing);
            flex-wrap: wrap;
            padding: 25px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
        }
        
        .control-btn {
            padding: 15px 25px;
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            color: var(--silver-ice);
            cursor: pointer;
            font-family: inherit;
            font-size: 0.75em;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            transition: all 0.3s;
            min-width: 120px;
        }
        
        .control-btn:hover {
            background: var(--silver-dark);
            border-color: var(--silver-light);
            transform: translateY(-2px);
        }
        
        .control-btn.stop {
            border-color: #4a2020;
            color: #8a4a4a;
        }
        
        .control-btn.stop:hover {
            background: #1a1010;
            border-color: #8a4a4a;
        }
        
        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1px;
            margin-bottom: var(--section-spacing);
            background: var(--border);
            border: 1px solid var(--border);
        }
        
        .stat-card {
            background: var(--bg-secondary);
            padding: 30px;
            text-align: center;
            transition: all 0.3s;
            position: relative;
        }
        
        .stat-card:hover {
            background: var(--silver-dark);
            transform: translateY(-3px);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: 300;
            color: var(--silver-ice);
            margin: 15px 0;
        }
        
        .stat-label {
            font-size: 0.7em;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        /* Main Content */
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: var(--section-spacing);
        }
        
        @media (max-width: 1024px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
        
        /* Terminal */
        .terminal-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .terminal-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--silver-dark);
        }
        
        .terminal-title {
            font-size: 0.75em;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--silver-ice);
        }
        
        .terminal-output {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            font-size: 0.75em;
            line-height: 1.8;
            color: var(--text-secondary);
        }
        
        .log-line {
            margin-bottom: 3px;
            white-space: pre-wrap;
            word-break: break-all;
        }
        
        .log-time {
            color: var(--silver-light);
            margin-right: 10px;
        }
        
        /* Attacks List */
        .attacks-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            height: 600px;
            display: flex;
            flex-direction: column;
        }
        
        .attacks-list {
            flex: 1;
            overflow-y: auto;
        }
        
        .attack-item {
            padding: 15px 20px;
            border-bottom: 1px solid var(--border);
            font-size: 0.75em;
            transition: all 0.3s;
        }
        
        .attack-item:hover {
            background: var(--silver-dark);
            transform: translateX(5px);
        }
        
        .badge {
            display: inline-block;
            padding: 3px 8px;
            font-size: 0.7em;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            border: 1px solid var(--silver-medium);
            background: var(--silver-dark);
            color: var(--silver-ice);
            margin-right: 5px;
        }
        
        .empty-state {
            text-align: center;
            padding: 60px;
            color: var(--text-secondary);
            font-size: 0.9em;
            letter-spacing: 0.1em;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 40px;
            margin-top: 80px;
            border-top: 1px solid var(--border);
            font-size: 0.7em;
            color: var(--text-secondary);
            letter-spacing: 0.15em;
            text-transform: uppercase;
        }
        
        .footer-social {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .social-icon {
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-secondary);
            border: 1px solid var(--silver-medium);
            color: var(--silver-ice);
            text-decoration: none;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .social-icon:hover {
            background: var(--silver-dark);
            border-color: var(--silver-bright);
            transform: translateY(-3px);
        }
    </style>
</head>
<body>
    <!-- ASCII Ripple Canvas -->
    <canvas id="ascii-ripple"></canvas>
    
    <div class="container">
        <!-- Navigation -->
        <div class="nav">
            <a href="/" class="nav-brand">SENTINEL</a>
            <div class="nav-links">
                <a href="/" class="nav-link">← Voltar</a>
                <span class="nav-link" onclick="showHelp()">Help</span>
                <span class="nav-link" onclick="startTour()">Tour</span>
                <a href="https://github.com/SEU_USUARIO_AQUI" target="_blank" class="nav-link">GitHub</a>
            </div>
        </div>
        
        <!-- Control Panel -->
        <div class="control-panel">
            <button class="control-btn" onclick="controlSystem('start', 'all')">▶ Start All</button>
            <button class="control-btn stop" onclick="controlSystem('stop', 'all')">■ Stop All</button>
            <button class="control-btn" onclick="controlSystem('restart', 'ssh')">↻ Restart SSH</button>
            <button class="control-btn" onclick="controlSystem('restart', 'http')">↻ Restart HTTP</button>
            <button class="control-btn" onclick="exportData('json')">Export JSON</button>
            <button class="control-btn" onclick="exportData('csv')">Export CSV</button>
        </div>
        
        <!-- Stats -->
        <div class="stats-grid" id="stats">
            <div class="stat-card">
                <div class="stat-label">Loading...</div>
                <div class="stat-value">...</div>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <div class="terminal-container">
                <div class="terminal-header">
                    <div class="terminal-title">Live Terminal</div>
                    <div class="terminal-title">LIVE</div>
                </div>
                <div class="terminal-output" id="terminal">
                    <div class="log-line">System initialized...</div>
                </div>
            </div>
            
            <div class="attacks-container">
                <div class="terminal-header">
                    <div class="terminal-title">Recent Attacks</div>
                    <div class="terminal-title">LIVE</div>
                </div>
                <div class="attacks-list" id="attacks">
                    <div class="empty-state">Loading...</div>
                </div>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <div class="footer-social">
                <a href="https://github.com/SEU_USUARIO_AQUI" target="_blank" class="social-icon">GH</a>
                <a href="mailto:SEU_EMAIL_AQUI" class="social-icon">@</a>
            </div>
            <p>SENTINEL v1.0 // Monochrome Edition</p>
        </div>
    </div>
    
    <script>
        // ============= ASCII RIPPLE EFFECT =============
        const canvas = document.getElementById('ascii-ripple');
        const ctx = canvas.getContext('2d');
        const asciiChars = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@'];
        const fontSize = 10;
        let columns, rows;
        let grid = [];
        let ripples = [];
        
        function initGrid() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            columns = Math.floor(canvas.width / fontSize);
            rows = Math.floor(canvas.height / fontSize);
            grid = [];
            for (let y = 0; y < rows; y++) {
                grid[y] = [];
                for (let x = 0; x < columns; x++) {
                    grid[y][x] = 0;
                }
            }
        }
        
        function createRipple(x, y) {
            ripples.push({
                x: x,
                y: y,
                radius: 0,
                maxRadius: 100,
                speed: 2,
                life: 1.0
            });
        }
        
        function updateRipples() {
            for (let i = ripples.length - 1; i >= 0; i--) {
                const ripple = ripples[i];
                ripple.radius += ripple.speed;
                ripple.life -= 0.02;
                if (ripple.life <= 0 || ripple.radius > ripple.maxRadius) {
                    ripples.splice(i, 1);
                }
            }
        }
        
        function applyRipples() {
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < columns; x++) {
                    grid[y][x] *= 0.95;
                }
            }
            
            for (const ripple of ripples) {
                const centerX = ripple.x / fontSize;
                const centerY = ripple.y / fontSize;
                const radius = ripple.radius / fontSize;
                
                for (let y = 0; y < rows; y++) {
                    for (let x = 0; x < columns; x++) {
                        const dx = x - centerX;
                        const dy = y - centerY;
                        const distance = Math.sqrt(dx * dx + dy * dy);
                        if (Math.abs(distance - radius) < 1) {
                            const intensity = ripple.life * (1 - distance / ripple.maxRadius * fontSize);
                            grid[y][x] = Math.max(grid[y][x], intensity);
                        }
                    }
                }
            }
        }
        
        function render() {
            ctx.fillStyle = '#0a0a0a';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.font = fontSize + 'px monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            
            for (let y = 0; y < rows; y++) {
                for (let x = 0; x < columns; x++) {
                    const intensity = grid[y][x];
                    if (intensity > 0.01) {
                        const charIndex = Math.floor(intensity * (asciiChars.length - 1));
                        const char = asciiChars[Math.min(charIndex, asciiChars.length - 1)];
                        const brightness = Math.floor(128 + intensity * 127);
                        ctx.fillStyle = `rgb(${brightness}, ${brightness}, ${brightness})`;
                        ctx.fillText(char, x * fontSize + fontSize / 2, y * fontSize + fontSize / 2);
                    }
                }
            }
        }
        
        function animate() {
            updateRipples();
            applyRipples();
            render();
            requestAnimationFrame(animate);
        }
        
        window.addEventListener('resize', initGrid);
        window.addEventListener('mousemove', (e) => {
            if (Math.random() < 0.3) {
                createRipple(e.clientX, e.clientY);
            }
        });
        window.addEventListener('click', (e) => {
            createRipple(e.clientX, e.clientY);
        });
        
        setInterval(() => {
            if (Math.random() < 0.5) {
                createRipple(Math.random() * canvas.width, Math.random() * canvas.height);
            }
        }, 3000);
        
        initGrid();
        animate();
        
        // ============= SENTINEL FUNCTIONS =============
        async function controlSystem(action, service) {
            try {
                const response = await fetch('/api/api/control', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action, service })
                });
                addLog(`System ${action} ${service}`, 'success');
                updateStats();
            } catch (error) {
                addLog(`Error: ${error}`, 'error');
            }
        }
        
        async function exportData(format) {
            try {
                const response = await fetch(`/api/api/export?format=${format}`);
                const data = await response.json();
                
                if (format === 'json') {
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `sentinel_export_${new Date().getTime()}.json`;
                    a.click();
                } else if (format === 'csv') {
                    const blob = new Blob([data.data], { type: 'text/csv' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `sentinel_export_${new Date().getTime()}.csv`;
                    a.click();
                }
                addLog(`Data exported as ${format.toUpperCase()}`, 'success');
            } catch (error) {
                addLog(`Export error: ${error}`, 'error');
            }
        }
        
        function addLog(message, type = 'info') {
            const terminal = document.getElementById('terminal');
            const logLine = document.createElement('div');
            logLine.className = 'log-line';
            const time = new Date().toLocaleTimeString();
            logLine.innerHTML = `<span class="log-time">[${time}]</span>${message}`;
            terminal.appendChild(logLine);
            terminal.scrollTop = terminal.scrollHeight;
            while (terminal.children.length > 100) {
                terminal.removeChild(terminal.firstChild);
            }
        }
        
        async function updateStats() {
            try {
                const response = await fetch('/api/api/stats');
                const data = await response.json();
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-label">Total Attacks</div>
                        <div class="stat-value">${data.total_attacks}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Unique IPs</div>
                        <div class="stat-value">${data.unique_ips}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Last 5 min</div>
                        <div class="stat-value">${data.recent_attacks_5min}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">SSH Status</div>
                        <div class="stat-value">${data.system_status.ssh_honeypot ? 'ON' : 'OFF'}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">HTTP Status</div>
                        <div class="stat-value">${data.system_status.http_honeypot ? 'ON' : 'OFF'}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Uptime</div>
                        <div class="stat-value" style="font-size: 1.2em;">${data.system_status.uptime}</div>
                    </div>
                `;
            } catch (error) {
                console.error('Error updating stats:', error);
            }
        }
        
        async function updateAttacks() {
            try {
                const response = await fetch('/api/api/attacks?limit=20');
                const attacks = await response.json();
                if (attacks.length === 0) {
                    document.getElementById('attacks').innerHTML = '<div class="empty-state">No attacks detected yet</div>';
                    return;
                }
                const attacksHTML = attacks.map(attack => {
                    let badge = attack.honeypot_type === 'ssh' ? '<span class="badge">SSH</span>' : '<span class="badge">HTTP</span>';
                    return `
                        <div class="attack-item">
                            <div>${badge} ${attack.source_ip}:${attack.source_port}</div>
                            <div style="color: var(--text-secondary); margin-top: 3px;">
                                ${new Date(attack.timestamp).toLocaleTimeString()}
                                ${attack.username ? `| ${attack.username}` : ''}
                                ${attack.password ? `:${attack.password}` : ''}
                            </div>
                        </div>
                    `;
                }).join('');
                document.getElementById('attacks').innerHTML = attacksHTML;
            } catch (error) {
                console.error('Error updating attacks:', error);
            }
        }
        
        function showHelp() {
            alert('SENTINEL HELP\\n\\n1. Use os botões de controle para gerenciar os honeypots\\n2. Monitore os ataques em tempo real no terminal\\n3. Veja estatísticas detalhadas nos cards acima\\n4. Exporte dados para análise externa');
        }
        
        function startTour() {
            const steps = [
                'Bem-vindo ao Dashboard do Sentinel!',
                'Aqui você controla os honeypots que capturam ataques',
                'O terminal mostra tudo que acontece em tempo real',
                'A lista mostra os ataques recentes com detalhes',
                'Use os botões de exportação para baixar os dados',
                'Clique em Help para ver este guia novamente'
            ];
            let step = 0;
            function showStep() {
                if (step < steps.length) {
                    alert(`Tour (${step + 1}/${steps.length})\\n\\n${steps[step]}`);
                    step++;
                    setTimeout(showStep, 500);
                }
            }
            showStep();
        }
        
        updateStats();
        updateAttacks();
        addLog('System online', 'success');
        addLog('Dashboard loaded', 'info');
        addLog('Monitoring started', 'success');
        
        setInterval(() => {
            updateStats();
            updateAttacks();
        }, 5000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return LANDING_PAGE

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    return DASHBOARD

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
