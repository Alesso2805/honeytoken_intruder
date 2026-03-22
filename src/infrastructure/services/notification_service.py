import requests
import json
from ...domain.entities import Alert

class NotificationService:
    """External service adapter for Discord Webhooks with GeoIP support"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def _get_geoip_data(self, ip: str) -> dict:
        """Fetch location data for a given IP address"""
        if ip in ['127.0.0.1', 'localhost', '::1']:
            return {"status": "success", "country": "Local Lab", "city": "Internal", "isp": "Development Environment"}
            
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {}

    def send_alert(self, alert: Alert):
        """Send formatted alert payload to Discord with GeoIP insights"""
        
        geo = self._get_geoip_data(alert.attacker_ip)
        location = f"{geo.get('city', 'Unknown')}, {geo.get('country', 'Unknown')}"
        isp = geo.get('isp', 'Unknown ISP')

        payload = {
            "embeds": [{
                "title": "🚨 HONEYTOKEN TRIGGERED 🚨",
                "color": 15158332,
                "fields": [
                    {"name": "Target Path", "value": f"`{alert.target_route}`", "inline": True},
                    {"name": "Attacker IP", "value": f"`{alert.attacker_ip}`", "inline": True},
                    {"name": "Location 🌍", "value": f"`{location}`", "inline": True},
                    {"name": "ISP 🏢", "value": f"`{isp}`", "inline": True},
                    {"name": "User-Agent", "value": f"```\n{alert.user_agent}\n```", "inline": False},
                    {"name": "Timestamp", "value": f"`{alert.timestamp.isoformat()}`", "inline": True}
                ],
                "footer": {"text": "Honeytoken Detection System • Sentinel AI"}
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
