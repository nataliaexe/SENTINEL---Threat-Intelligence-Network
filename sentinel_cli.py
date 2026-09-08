#!/usr/bin/env python3
import sys
import os
import json
import argparse
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_status():
    """Verificar status do sistema"""
    import requests
    
    try:
        response = requests.get('http://localhost:8000/', timeout=2)
        if response.status_code == 200:
            print("✅ Sentinel API: Online")
        else:
            print("⚠️ Sentinel API: Status desconhecido")
    except:
        print("❌ Sentinel API: Offline")
    
    try:
        response = requests.get('http://localhost:8000/api/stats', timeout=2)
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Total de ataques: {stats['total_attacks']}")
            print(f"🌍 IPs únicos: {stats['unique_ips']}")
            print(f"⚡ Últimos 5 min: {stats['recent_attacks_5min']}")
    except:
        pass

def list_attacks(limit=10):
    """Listar últimos ataques"""
    import requests
    
    try:
        response = requests.get(f'http://localhost:8000/api/attacks?limit={limit}', timeout=5)
        if response.status_code == 200:
            attacks = response.json()
            
            if not attacks:
                print("Nenhum ataque registrado.")
                return
            
            print(f"\n📋 Últimos {len(attacks)} ataques:")
            print("=" * 80)
            
            for attack in attacks:
                print(f"""
⏰ {attack['timestamp']}
🌐 IP: {attack['source_ip']}:{attack['source_port']}
📡 Protocolo: {attack['protocol']}
👤 Usuário: {attack.get('username', 'N/A')}
🔑 Senha: {attack.get('password', 'N/A')}
📍 Localização: {attack.get('city', 'Unknown')}, {attack.get('country', 'Unknown')}
📝 Payload: {attack.get('payload', 'N/A')[:100]}
{'=' * 80}""")
    except Exception as e:
        print(f"❌ Erro: {e}")

def generate_report():
    """Gerar relatório"""
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils'))
    from report_generator import ReportGenerator
    
    generator = ReportGenerator()
    report = generator.generate_report(hours=24)
    
    if report:
        generator.print_report(report)
        filepath = generator.save_report(report)
        print(f"\n✅ Relatório salvo em: {filepath}")
    else:
        print("Nenhum ataque no período especificado.")

def monitor_live():
    """Monitorar em tempo real"""
    import requests
    import time
    
    print("🔍 Monitorando ataques em tempo real...")
    print("Pressione Ctrl+C para parar.")
    print("=" * 60)
    
    last_id = 0
    
    while True:
        try:
            response = requests.get('http://localhost:8000/api/attacks?limit=1', timeout=2)
            if response.status_code == 200:
                attacks = response.json()
                if attacks and attacks[0]['id'] > last_id:
                    attack = attacks[0]
                    last_id = attack['id']
                    
                    print(f"""
🚨 NOVO ATAQUE DETECTADO!
⏰ {attack['timestamp']}
🌐 IP: {attack['source_ip']}
📡 Tipo: {attack['honeypot_type']}
👤 Usuário: {attack.get('username', 'N/A')}
🔑 Senha: {attack.get('password', 'N/A')}
{'=' * 60}""")
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoramento encerrado.")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            time.sleep(5)

def main():
    parser = argparse.ArgumentParser(description='Sentinel CLI - Honeypot Intelligence Network')
    parser.add_argument('command', choices=['status', 'attacks', 'report', 'monitor'],
                       help='Comando a executar')
    parser.add_argument('--limit', type=int, default=10,
                       help='Número de itens a mostrar (padrão: 10)')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        check_status()
    elif args.command == 'attacks':
        list_attacks(args.limit)
    elif args.command == 'report':
        generate_report()
    elif args.command == 'monitor':
        monitor_live()

if __name__ == "__main__":
    main()
