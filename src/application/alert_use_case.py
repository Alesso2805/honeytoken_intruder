import threading
from ..domain.entities import Alert
from ..domain.repositories import AlertRepository
from ..infrastructure.services.notification_service import NotificationService
from datetime import datetime
from typing import Dict

class TriggerAlertUseCase:
    """Core logic to process and notify security alerts"""
    
    def __init__(self, alert_repo: AlertRepository, notification_service: NotificationService):
        self.alert_repo = alert_repo
        self.notification_service = notification_service

    def execute(self, route: str, ip: str, user_agent: str, headers: Dict[str, str]) -> Alert:
        """Create and process a security alert asynchronously"""
        
        alert = Alert(
            target_route=route,
            attacker_ip=ip,
            user_agent=user_agent,
            headers=headers,
            timestamp=datetime.utcnow()
        )
        
        saved_alert = self.alert_repo.save(alert)
        
        threading.Thread(
            target=self.notification_service.send_alert,
            args=(saved_alert,),
            daemon=True
        ).start()
        
        return saved_alert
