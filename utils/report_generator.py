import json
import os
import sys
from datetime import datetime, timedelta
import sqlalchemy as sa

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import AttackAttempt, SessionLocal

class ReportGenerator:
    def __init__(self):
        self.db = SessionLocal()
    
    def generate_report(self, hours=24):
        """Gerar relatório dos últimos X horas"""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        # Buscar ataques do período
        attacks = self.db.query(AttackAttempt)\
            .filter(AttackAttempt.timestamp >= since)\
            .all()
        
        if not attacks:
            return None
        
        # Análises
        total = len(attacks)
        unique_ips = set(a.source_ip for a in attacks)
        
        # Agrupar por tipo
        by_type = {}
        for attack in attacks:
            by_type[attack.honeypot_type] = by_type.get(attack.honeypot_type, 0) + 1
        
        # Agrupar por país
        by_country = {}
        for attack in attacks:
            country = attack.country or 'Unknown'
            by_country[country] = by_country.get(country, 0) + 1
        
        # Credenciais mais comuns
        credentials = {}
        for attack in attacks:
            if attack.username and attack.password:
                cred = f"{attack.username}:{attack.password}"
                credentials[cred] = credentials.get(cred, 0) + 1
        
        top_credentials = sorted(credentials.items(), key=lambda x: x[1], reverse=True)[:10]
        
        report = {
            'report_time': datetime.utcnow().isoformat(),
            'period_hours': hours,
            'summary': {
                'total_attacks': total,
                'unique_ips': len(unique_ips),
                'by_type': by_type,
                'by_country': by_country,
            },
            'top_credentials': top_credentials,
            'recent_attacks': [
                {
                    'timestamp': a.timestamp.isoformat(),
                    'ip': a.source_ip,
                    'type': a.honeypot_type,
                    'username': a.username,
                    'password': a.password,
                    'country': a.country,
                    'city': a.city
                }
                for a in attacks[:20]
            ]
        }
        
        return report
    
    def save_report(self, report, filename=None):
        """Salvar relatório em JSON"""
        if not filename:
            filename = f"report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'reports'
        )
        os.makedirs(report_dir, exist_ok=True)
        
        filepath = os.path.join(report_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    def print_report(self, report):
        """Imprimir relatório formatado"""
        if not report:
            print("Nenhum ataque no período especificado.")
            return
        
        print("""
╔══════════════════════════════════════╗
║        RELATÓRIO DE SEGURANÇA        ║
╚══════════════════════════════════════╝
""")
        print(f"Período: Últimas {report['period_hours']} horas")
        print(f"Total de ataques: {report['summary']['total_attacks']}")
        print(f"IPs únicos: {report['summary']['unique_ips']}")
        
        print("\n Ataques por tipo:")
        for type_, count in report['summary']['by_type'].items():
            print(f"  - {type_}: {count}")
        
        print("\n Ataques por país:")
        for country, count in report['summary']['by_country'].items():
            print(f"  - {country}: {count}")
        
        if report['top_credentials']:
            print("\n Credenciais mais usadas:")
            for cred, count in report['top_credentials']:
                print(f"  - {cred}: {count}x")

if __name__ == "__main__":
    generator = ReportGenerator()
    report = generator.generate_report(hours=1)
    generator.print_report(report)
    
    if report:
        filepath = generator.save_report(report)
        print(f"\n Relatório salvo em: {filepath}")
