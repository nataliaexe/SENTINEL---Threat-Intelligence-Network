import requests
import json
import logging
from datetime import datetime
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AlertSystem:
    def __init__(self):
        self.logger = logging.getLogger('AlertSystem')
        self.webhook_url = None
        self.load_config()
    
    def load_config(self):
        """Carregar configurações de webhook"""
        config_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'config', 'alerts.json'
        )
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.webhook_url = config.get('discord_webhook') or config.get('telegram_webhook')
            except:
                pass
    
    def send_discord_alert(self, attack_data):
        """Enviar alerta para Discord"""
        if not self.webhook_url:
            return
        
        embed = {
            "title": " Novo Ataque Detectado!",
            "color": 15158332,  # Vermelho
            "fields": [
                {"name": "IP", "value": attack_data.get('source_ip', 'Unknown'), "inline": True},
                {"name": "Porta", "value": str(attack_data.get('source_port', 'Unknown')), "inline": True},
                {"name": "Protocolo", "value": attack_data.get('protocol', 'Unknown'), "inline": True},
                {"name": "Usuário", "value": attack_data.get('username', 'N/A'), "inline": True},
                {"name": "Senha", "value": attack_data.get('password', 'N/A'), "inline": True},
                {"name": "Localização", "value": f"{attack_data.get('city', 'Unknown')}, {attack_data.get('country', 'Unknown')}", "inline": True},
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if attack_data.get('payload'):
            embed["fields"].append({
                "name": "Payload",
                "value": attack_data['payload'][:200],
                "inline": False
            })
        
        try:
            response = requests.post(
                self.webhook_url,
                json={"embeds": [embed]},
                timeout=5
            )
            if response.status_code == 204:
                self.logger.info(" Alerta enviado para Discord")
        except Exception as e:
            self.logger.error(f"❌ Erro ao enviar alerta: {e}")
    
    def send_telegram_alert(self, attack_data, bot_token=None, chat_id=None):
        """Enviar alerta para Telegram"""
        if not bot_token or not chat_id:
            return
        
        message = f"""
 *NOVO ATAQUE DETECTADO*

 *IP:* `{attack_data.get('source_ip', 'Unknown')}`
 *Porta:* `{attack_data.get('source_port', 'Unknown')}`
 *Protocolo:* `{attack_data.get('protocol', 'Unknown')}`
 *Usuário:* `{attack_data.get('username', 'N/A')}`
 *Senha:* `{attack_data.get('password', 'N/A')}`
 *Localização:* `{attack_data.get('city', 'Unknown')}, {attack_data.get('country', 'Unknown')}`
 *Tempo:* `{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}`
"""
        
        if attack_data.get('payload'):
            message += f"\n *Payload:* `{attack_data['payload'][:100]}`"
        
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            response = requests.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                },
                timeout=5
            )
            if response.status_code == 200:
                self.logger.info(" Alerta enviado para Telegram")
        except Exception as e:
            self.logger.error(f" Erro ao enviar alerta Telegram: {e}")

# Singleton
alert_system = AlertSystem()
