import requests
import json
from datetime import datetime
import os
import sys

# Adicionar caminho do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GeoLocator:
    def __init__(self):
        self.cache = {}
        self.cache_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'logs', 'geo_cache.json'
        )
        self.load_cache()
    
    def load_cache(self):
        """Carregar cache de geolocalização"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.cache = json.load(f)
        except:
            self.cache = {}
    
    def save_cache(self):
        """Salvar cache de geolocalização"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except:
            pass
    
    def get_location(self, ip):
        """Obter localização de um IP"""
        # Verificar cache primeiro
        if ip in self.cache:
            return self.cache[ip]
        
        # IPs locais
        if ip in ['127.0.0.1', 'localhost', '::1']:
            location = {
                'country': 'Local',
                'city': 'Localhost',
                'latitude': 0,
                'longitude': 0
            }
        else:
            try:
                # Usar API gratuita de geolocalização
                response = requests.get(
                    f'http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon',
                    timeout=3
                )
                data = response.json()
                
                if data.get('status') == 'success':
                    location = {
                        'country': data.get('country', 'Unknown'),
                        'city': data.get('city', 'Unknown'),
                        'latitude': data.get('lat', 0),
                        'longitude': data.get('lon', 0)
                    }
                else:
                    location = {
                        'country': 'Unknown',
                        'city': 'Unknown',
                        'latitude': 0,
                        'longitude': 0
                    }
            except:
                location = {
                    'country': 'Unknown',
                    'city': 'Unknown',
                    'latitude': 0,
                    'longitude': 0
                }
        
        # Salvar no cache
        self.cache[ip] = location
        self.save_cache()
        
        return location
    
    def enrich_attack(self, attack_data):
        """Enriquecer dados de ataque com geolocalização"""
        location = self.get_location(attack_data.get('source_ip'))
        attack_data.update(location)
        return attack_data

# Singleton
geo_locator = GeoLocator()
