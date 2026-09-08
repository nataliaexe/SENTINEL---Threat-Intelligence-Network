import re
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RiskAnalyzer:
    def __init__(self):
        self.risk_patterns = {
            'high': [
                r'root',
                r'admin',
                r'SELECT.*FROM',
                r'UNION.*SELECT',
                r'<script>',
                r'\.\./',
                r'cmd\.exe',
                r'/bin/bash',
            ],
            'medium': [
                r'password',
                r'login',
                r'config',
                r'\.env',
                r'wp-admin',
                r'phpmyadmin',
            ]
        }
    
    def calculate_risk_score(self, attack_data):
        """Calcular score de risco (0-100)"""
        score = 0
        
        # Analisar payload
        payload = attack_data.get('payload', '').lower()
        username = attack_data.get('username', '').lower()
        password = attack_data.get('password', '').lower()
        
        combined = f"{payload} {username} {password}"
        
        # Verificar padrões de alto risco
        for pattern in self.risk_patterns['high']:
            if re.search(pattern, combined):
                score += 30
                break
        
        # Verificar padrões de médio risco
        for pattern in self.risk_patterns['medium']:
            if re.search(pattern, combined):
                score += 15
                break
        
        # Pontuação por tipo de honeypot
        if attack_data.get('honeypot_type') == 'ssh':
            if username == 'root':
                score += 20
            if password in ['123456', 'password', 'admin', 'root', 'toor']:
                score += 10
        elif attack_data.get('honeypot_type') == 'http':
            if 'sql' in payload:
                score += 25
            if 'xss' in payload:
                score += 20
        
        # Limitar score
        return min(score, 100)
    
    def get_risk_level(self, score):
        """Obter nível de risco baseado no score"""
        if score >= 70:
            return 'CRÍTICO'
        elif score >= 40:
            return 'ALTO'
        elif score >= 20:
            return 'MÉDIO'
        else:
            return 'BAIXO'
    
    def analyze_attack(self, attack_data):
        """Analisar ataque completo"""
        score = self.calculate_risk_score(attack_data)
        level = self.get_risk_level(score)
        
        return {
            'risk_score': score,
            'risk_level': level,
            'recommendations': self.get_recommendations(score, attack_data)
        }
    
    def get_recommendations(self, score, attack_data):
        """Gerar recomendações baseadas no risco"""
        recommendations = []
        
        if score >= 70:
            recommendations.append("🚨 BLOQUEAR IP imediatamente")
            recommendations.append("🔍 Investigar origem do ataque")
            recommendations.append("📊 Reportar para threat intelligence")
        elif score >= 40:
            recommendations.append("⚠️ Monitorar IP de perto")
            recommendations.append("🔒 Reforçar autenticação")
        else:
            recommendations.append("📝 Registrar e continuar monitorando")
        
        if attack_data.get('honeypot_type') == 'ssh':
            recommendations.append("🔑 Implementar 2FA")
            recommendations.append("🚫 Desabilitar login como root")
        elif attack_data.get('honeypot_type') == 'http':
            recommendations.append("🛡️ Atualizar WAF")
            recommendations.append("📝 Revisar código para vulnerabilidades")
        
        return recommendations

# Singleton
risk_analyzer = RiskAnalyzer()
