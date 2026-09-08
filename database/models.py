from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os

# Adicionar caminho do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import config

Base = declarative_base()

class AttackAttempt(Base):
    __tablename__ = 'attack_attempts'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String(50))
    source_port = Column(Integer)
    destination_port = Column(Integer)
    protocol = Column(String(20))
    username = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    payload = Column(Text)
    honeypot_type = Column(String(50))
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    risk_score = Column(Float, default=0.0)

class HoneypotInstance(Base):
    __tablename__ = 'honeypot_instances'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(50))
    ip = Column(String(50))
    port = Column(Integer)
    status = Column(String(20), default='active')
    started_at = Column(DateTime, default=datetime.utcnow)
    last_attack = Column(DateTime, nullable=True)
    total_attacks = Column(Integer, default=0)

# Criar engine e sessão
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
