
# SENTINEL - Threat Intelligence Network

![Version](https://img.shields.io/badge/version-1.0.0-silver)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> Sistema avançado de honeypots que detecta, analisa e monitora tentativas de ataques cibernéticos em tempo real.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Acesse_Aqui-silver)](https://sentinel.onrender.com)


##  Live Demo

O projeto está rodando em tempo real no Render:

| Interface | Link |
|-----------|------|
| Landing Page | [Acessar](https://sentinel-threat-intelligence-network.onrender.com/) |
| Dashboard | [Acessar](https://sentinel-threat-intelligence-network.onrender.com/dashboard) |
| API Stats | [Acessar](https://sentinel-threat-intelligence-network.onrender.com/api/stats) |
| Documentação | [Acessar](https://sentinel-threat-intelligence-network.onrender.com/docs) |

> Nota: O servidor gratuito do Render entra em modo de hibernação após 15 minutos sem atividade. A primeira requisição pode demorar 30-60 segundos para "acordar" o servidor.
---

## Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Demonstração](#-demonstração)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [API Reference](#-api-reference)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)
- [Contribuição](#-contribuição)
- [Licença](#-licença)
- [Contato](#-contato)

---

## Sobre o Projeto

O **Sentinel** é uma rede de honeypots que simula serviços vulneráveis para atrair atacantes e coletar inteligência sobre suas técnicas. O sistema captura tentativas de invasão, analisa padrões de ataque e fornece visualização em tempo real através de um dashboard elegante com efeito ASCII Ripple.

### Por que honeypots?

-  **Detecção precoce** de ameaças
-  **Coleta de inteligência** sobre atacantes
-  **Proteção** de sistemas reais
-  **Aprendizado** sobre técnicas de ataque
-  **Pesquisa** em segurança cibernética

---

##  Funcionalidades

###  Honeypot SSH
- Simula servidor SSH vulnerável (OpenSSH 7.9)
- Captura tentativas de login
- Registra usuários e senhas tentados
- Geolocalização de IPs de origem
- Múltiplas tentativas por conexão

###  Honeypot HTTP
- Simula servidor web com vulnerabilidades
- Detecta SQL Injection
- Detecta XSS (Cross-Site Scripting)
- Detecta Path Traversal
- Detecta Command Injection
- Detecta acesso a arquivos sensíveis

###  Dashboard em Tempo Real
- **Landing Page** explicativa e didática
- **Terminal ao vivo** com logs
- **Estatísticas** atualizadas automaticamente
- **Lista de ataques** recentes
- **Controle remoto** dos honeypots
- **Exportação** de dados (JSON/CSV)
- **Efeito ASCII Ripple** interativo
- **Design monocromático** minimalista

###  Inteligência de Ameaças
- Geolocalização automática de IPs
- Análise de padrões de ataque
- Classificação de risco
- Top credenciais usadas
- Análise temporal
- Análise por país

###  Análises Avançadas
- Estatísticas em tempo real
- Ataques por hora
- Ataques por tipo
- IPs únicos
- Uptime do sistema
- Exportação de dados

---

##  Demonstração

### Landing Page
![Landing Page](screenshots/landing.png)

Acesse `http://localhost:8888` para ver:
- Explicação do projeto
- Funcionalidades detalhadas
- Guia de uso
- FAQ interativo
- Links de contato

### Dashboard
![Dashboard](screenshots/dashboard.png)

Acesse `http://localhost:8888/dashboard` para ver:
- Controles dos honeypots
- Terminal em tempo real
- Estatísticas ao vivo
- Lista de ataques
- Botões de exportação

---

##  Arquitetura

```
┌─────────────────────────────────────────────────┐
│                   SENTINEL                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   SSH    │  │   HTTP   │  │   API    │       │
│  │ Honeypot │  │ Honeypot │  │  REST    │       │
│  │ :2222    │  │ :8080    │  │ :8000    │       │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘       │
│        │             │             │            │
│        └─────────────┼─────────────┘            │
│                      │                          │
│              ┌───────▼────────┐                 │
│              │   Database     │                 │
│              │   (SQLite)     │                 │
│              └───────┬────────┘                 │
│                      │                          │
│              ┌───────▼────────┐                 │
│              │   Dashboard    │                 │
│              │   :8888        │                 │
│              └────────────────┘                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Fluxo de Dados

1. **Atacante** tenta conectar ao honeypot
2. **Honeypot** captura a tentativa
3. **Geolocalização** enriquece os dados
4. **Database** armazena o ataque
5. **API** disponibiliza os dados
6. **Dashboard** exibe em tempo real

---

##  Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/nataliaexe/SENTINEL---Threat-Intelligence-Network.git
cd SENTINEL---Threat-Intelligence-Network

# 2. Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 5. Inicie o sistema
python3 main.py
```

### Instalação Rápida (Linux/Mac)

```bash
git clone https://github.com/nataliaexe/SENTINEL---Threat-Intelligence-Network.git
cd SENTINEL---Threat-Intelligence-Network
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

---

##  Como Usar

### 1. Iniciar o Sistema

```bash
python3 main.py
```

### 2. Acessar Interfaces

- **Landing Page:** http://localhost:8888
- **Dashboard:** http://localhost:8888/dashboard
- **API Docs:** http://localhost:8000/docs
- **API:** http://localhost:8000

### 3. Testar os Honeypots

#### SSH Honeypot
```bash
# Usando ssh client
ssh localhost -p 2222

# Ou usando Python
python3 test_ssh.py
```

#### HTTP Honeypot
```bash
# Simular ataque XSS
curl "http://localhost:8080/search?q=<script>alert('xss')</script>"

# Simular SQL Injection
curl "http://localhost:8080/page.php?id=1' OR '1'='1"

# Simular Path Traversal
curl "http://localhost:8080/../../etc/passwd"
```

### 4. Monitorar Ataques

```bash
# Usando CLI
python3 sentinel_cli.py status
python3 sentinel_cli.py attacks
python3 sentinel_cli.py monitor

# Ou via API
curl http://localhost:8000/api/stats
curl http://localhost:8000/api/attacks
```

### 5. Exportar Dados

```bash
# JSON
curl "http://localhost:8000/api/export?format=json" > attacks.json

# CSV
curl "http://localhost:8000/api/export?format=csv" > attacks.csv
```

---

##  API Reference

### Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Status do sistema |
| GET | `/api/stats` | Estatísticas gerais |
| GET | `/api/attacks` | Lista de ataques |
| GET | `/api/attacks?limit=10` | Ataques com limite |
| GET | `/api/attacks?honeypot_type=ssh` | Filtrar por tipo |
| POST | `/api/control` | Controlar honeypots |
| GET | `/api/export?format=json` | Exportar JSON |
| GET | `/api/export?format=csv` | Exportar CSV |
| GET | `/api/logs/{type}` | Ver logs |
| GET | `/api/analytics` | Análises avançadas |

### Exemplo de Resposta

```json
{
  "total_attacks": 150,
  "unique_ips": 45,
  "recent_attacks_5min": 3,
  "hour_attacks": 12,
  "top_usernames": [
    ["root", 25],
    ["admin", 18],
    ["test", 10]
  ],
  "attacks_by_type": {
    "ssh": 80,
    "http": 70
  },
  "system_status": {
    "running": true,
    "ssh_honeypot": true,
    "http_honeypot": true,
    "uptime": "2:30:45"
  }
}
```

---

##  Estrutura do Projeto

```
sentinel/
├── core/
│   ├── __init__.py
│   └── api.py              # API REST
│
├── honeypots/
│   ├── __init__.py
│   ├── ssh_honeypot.py     # Honeypot SSH
│   └── http_honeypot.py    # Honeypot HTTP
│
├── dashboard/
│   ├── __init__.py
│   └── server.py           # Dashboard web
│
├── database/
│   ├── __init__.py
│   └── models.py           # Modelos SQLAlchemy
│
├── utils/
│   ├── __init__.py
│   ├── geo_locator.py      # Geolocalização
│   └── risk_analyzer.py    # Análise de risco
│
├── config/
│   ├── __init__.py
│   └── settings.py         # Configurações
│
├── logs/                   # Logs do sistema
├── main.py                 # Entry point
├── sentinel_cli.py         # CLI tool
├── test_ssh.py             # Teste SSH
├── simulate_attacks.py     # Simulador de ataques
├── requirements.txt        # Dependências
├── .env.example           # Exemplo de config
├── .gitignore
├── LICENSE
└── README.md
```

---

##  Tecnologias

- **Python 3.8+** - Linguagem principal
- **FastAPI** - Framework web
- **Uvicorn** - Servidor ASGI
- **SQLAlchemy** - ORM
- **SQLite** - Banco de dados
- **HTML/CSS/JavaScript** - Frontend
- **Canvas API** - Efeito ASCII Ripple

---

##  Contribuição

Contribuições são bem-vindas! Siga os passos:

1. **Fork** o projeto
2. **Crie** uma branch (`git checkout -b feature/nova-feature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. **Push** para a branch (`git push origin feature/nova-feature`)
5. **Abra** um Pull Request

### Diretrizes

- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Mantenha commits descritivos

---

##  Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2024 Natália

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

##  Contato

- **GitHub:** [@nataliaexe](https://github.com/nataliaexe)
- **Email:** [nataliavargas.exe@email.com](mailto:nataliavargas.exe@email.com)

---

##  Aviso Legal

**Este projeto é para fins educacionais e de pesquisa apenas.**

- Use apenas em sistemas que você possui ou tem autorização
- Não use para atividades maliciosas
- Respeite as leis locais e internacionais
- Os autores não são responsáveis pelo uso indevido

---

##  Agradecimentos

- Comunidade de cybersecurity
- Desenvolvedores de honeypots open source
- Todos que contribuíram para o projeto

---

**Feito por [Natália](https://github.com/nataliaexe)**

[⬆ Voltar ao topo](#-sentinel---threat-intelligence-network)
