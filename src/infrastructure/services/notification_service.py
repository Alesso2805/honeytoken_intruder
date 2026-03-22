import requests
import json
from ...domain.entities import Alert

class NotificationService:
    """External service adapter for Discord Webhooks"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_alert(self, alert: Alert):
        """Send formatted alert payload to Discord"""
        
        payload = {
            "embeds": [{
                "title": "🚨 HONEYTOKEN TRIGGERED 🚨",
                "color": 15158332,  
                "fields": [
                    {"name": "Target Path", "value": f"`{alert.target_route}`", "inline": True},
                    {"name": "Attacker IP", "value": f"`{alert.attacker_ip}`", "inline": True},
                    {"name": "User-Agent", "value": f"`{alert.user_agent}`", "inline": False},
                    {"name": "Timestamp", "value": f"`{alert.timestamp.isoformat()}`", "inline": True}
                ],
                "footer": {"text": "Honeytoken Detection System"}
            }]
        }
        
        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send notification: {e}")
