import requests
import time
import json
from datetime import datetime

def monitor_attacks():
    print("🔍 Monitorando ataques em tempo real...")
    print("=" * 60)
    
    last_count = 0
    
    while True:
        try:
            # Buscar estatísticas
            response = requests.get('http://localhost:8000/api/stats')
            stats = response.json()
            
            # Verificar se há novos ataques
            if stats['total_attacks'] > last_count:
                new_attacks = stats['total_attacks'] - last_count
                print(f"\n🚨 {new_attacks} novo(s) ataque(s) detectado(s)!")
                print(f"📊 Total: {stats['total_attacks']}")
                print(f"🌍 IPs únicos: {stats['unique_ips']}")
                print(f"⚡ Últimos 5 min: {stats['recent_attacks_5min']}")
                
                if stats['top_usernames']:
                    print("\n👤 Usuários mais tentados:")
                    for user, count in stats['top_usernames']:
                        if user:
                            print(f"   - {user}: {count} tentativas")
                
                print("=" * 60)
                last_count = stats['total_attacks']
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n🛑 Monitoramento encerrado")
            break
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_attacks()
