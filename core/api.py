from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List
import sys
import os
import json
import asyncio
import subprocess

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import AttackAttempt, HoneypotInstance, get_db, SessionLocal

app = FastAPI(title="Sentinel API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado do sistema
system_state = {
    "running": True,
    "ssh_honeypot": True,
    "http_honeypot": True,
    "started_at": datetime.utcnow(),
    "uptime": 0,
    "total_connections": 0,
    "active_connections": 0
}

# Modelos Pydantic
class SystemControl(BaseModel):
    action: str  # start, stop, restart
    service: Optional[str] = None  # all, ssh, http

class ConfigUpdate(BaseModel):
    ssh_port: Optional[int] = 2222
    http_port: Optional[int] = 8080
    alert_threshold: Optional[int] = 50

@app.get("/")
async def root():
    return {
        "name": "Sentinel API",
        "version": "1.0.0",
        "status": "operational" if system_state["running"] else "stopped",
        "timestamp": datetime.utcnow(),
        "uptime": str(datetime.utcnow() - system_state["started_at"])
    }

@app.get("/api/attacks")
async def get_attacks(
    limit: int = 100,
    offset: int = 0,
    honeypot_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AttackAttempt)
    
    if honeypot_type:
        query = query.filter(AttackAttempt.honeypot_type == honeypot_type)
    
    attacks = query.order_by(AttackAttempt.timestamp.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    return attacks

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    total_attacks = db.query(AttackAttempt).count()
    unique_ips = db.query(AttackAttempt.source_ip).distinct().count()
    
    # Últimos 5 minutos
    last_5min = datetime.utcnow() - timedelta(minutes=5)
    recent_attacks = db.query(AttackAttempt)\
        .filter(AttackAttempt.timestamp >= last_5min)\
        .count()
    
    # Última hora
    last_hour = datetime.utcnow() - timedelta(hours=1)
    hour_attacks = db.query(AttackAttempt)\
        .filter(AttackAttempt.timestamp >= last_hour)\
        .count()
    
    # Top usuários
    top_usernames = db.query(
        AttackAttempt.username,
        func.count(AttackAttempt.username)
    ).group_by(AttackAttempt.username)\
     .order_by(func.count(AttackAttempt.username).desc())\
     .limit(5)\
     .all()
    
    # Ataques por tipo
    attacks_by_type = db.query(
        AttackAttempt.honeypot_type,
        func.count(AttackAttempt.honeypot_type)
    ).group_by(AttackAttempt.honeypot_type)\
     .all()
    
    # Ataques por hora (últimas 24h)
    last_24h = datetime.utcnow() - timedelta(hours=24)
    attacks_24h = db.query(AttackAttempt)\
        .filter(AttackAttempt.timestamp >= last_24h)\
        .all()
    
    hourly_data = {}
    for attack in attacks_24h:
        hour = attack.timestamp.strftime('%H:00')
        hourly_data[hour] = hourly_data.get(hour, 0) + 1
    
    return {
        "total_attacks": total_attacks,
        "unique_ips": unique_ips,
        "recent_attacks_5min": recent_attacks,
        "hour_attacks": hour_attacks,
        "top_usernames": [(u, c) for u, c in top_usernames if u],
        "attacks_by_type": dict(attacks_by_type),
        "hourly_data": hourly_data,
        "system_status": {
            "running": system_state["running"],
            "ssh_honeypot": system_state["ssh_honeypot"],
            "http_honeypot": system_state["http_honeypot"],
            "uptime": str(datetime.utcnow() - system_state["started_at"])
        }
    }

@app.post("/api/control")
async def control_system(control: SystemControl):
    """Controlar o sistema"""
    action = control.action.lower()
    service = control.service or "all"
    
    if action == "stop":
        if service in ["all", "ssh"]:
            system_state["ssh_honeypot"] = False
        if service in ["all", "http"]:
            system_state["http_honeypot"] = False
        if service == "all":
            system_state["running"] = False
        
        return {"status": "stopped", "service": service}
    
    elif action == "start":
        if service in ["all", "ssh"]:
            system_state["ssh_honeypot"] = True
        if service in ["all", "http"]:
            system_state["http_honeypot"] = True
        if service == "all":
            system_state["running"] = True
        
        return {"status": "started", "service": service}
    
    elif action == "restart":
        return {"status": "restarting", "service": service}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

@app.get("/api/export")
async def export_data(format: str = "json", db: Session = Depends(get_db)):
    """Exportar dados em diferentes formatos"""
    attacks = db.query(AttackAttempt).all()
    
    if format == "json":
        data = [
            {
                "id": a.id,
                "timestamp": a.timestamp.isoformat(),
                "source_ip": a.source_ip,
                "source_port": a.source_port,
                "protocol": a.protocol,
                "username": a.username,
                "password": a.password,
                "payload": a.payload,
                "honeypot_type": a.honeypot_type,
                "country": a.country,
                "city": a.city,
                "risk_score": a.risk_score
            }
            for a in attacks
        ]
        return {"total": len(data), "attacks": data}
    
    elif format == "csv":
        csv_data = "id,timestamp,source_ip,source_port,protocol,username,password,honeypot_type,country,city,risk_score\n"
        for a in attacks:
            csv_data += f"{a.id},{a.timestamp},{a.source_ip},{a.source_port},{a.protocol},{a.username},{a.password},{a.honeypot_type},{a.country},{a.city},{a.risk_score}\n"
        return {"format": "csv", "data": csv_data}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid format")

@app.get("/api/logs/{log_type}")
async def get_logs(log_type: str, lines: int = 50):
    """Obter logs em tempo real"""
    log_files = {
        "ssh": "logs/ssh_honeypot.log",
        "http": "logs/http_honeypot.log",
        "system": "logs/sentinel.log"
    }
    
    if log_type not in log_files:
        raise HTTPException(status_code=404, detail="Log not found")
    
    log_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        log_files[log_type]
    )
    
    if not os.path.exists(log_path):
        return {"lines": [], "message": "No logs yet"}
    
    try:
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
            last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return {
            "lines": [line.strip() for line in last_lines],
            "total_lines": len(all_lines)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    """Análises avançadas"""
    # Ataques por país
    attacks_by_country = db.query(
        AttackAttempt.country,
        func.count(AttackAttempt.country)
    ).group_by(AttackAttempt.country)\
     .order_by(func.count(AttackAttempt.country).desc())\
     .limit(10)\
     .all()
    
    # Credenciais mais comuns
    common_credentials = db.query(
        AttackAttempt.username,
        AttackAttempt.password,
        func.count(AttackAttempt.id)
    ).filter(
        AttackAttempt.username.isnot(None),
        AttackAttempt.password.isnot(None)
    ).group_by(
        AttackAttempt.username,
        AttackAttempt.password
    ).order_by(
        func.count(AttackAttempt.id).desc()
    ).limit(10).all()
    
    # Análise temporal
    attacks_by_day = db.query(
        func.date(AttackAttempt.timestamp),
        func.count(AttackAttempt.id)
    ).group_by(
        func.date(AttackAttempt.timestamp)
    ).all()
    
    return {
        "attacks_by_country": [(c, cnt) for c, cnt in attacks_by_country if c],
        "common_credentials": [
            {"username": u, "password": p, "count": cnt}
            for u, p, cnt in common_credentials
        ],
        "attacks_by_day": [
            {"date": str(d), "count": cnt}
            for d, cnt in attacks_by_day
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
