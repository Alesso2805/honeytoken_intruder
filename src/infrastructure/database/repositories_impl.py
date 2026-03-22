from typing import List, Optional
from .models import db, AlertDB, HoneytokenDB, BannedIPDB
from ...domain.entities import Alert, Honeytoken, BannedIP
from ...domain.repositories import AlertRepository, HoneytokenRepository, BannedIPRepository

class SQLAlchemyAlertRepository(AlertRepository):
    def save(self, alert: Alert) -> Alert:
        alert_db = AlertDB(
            target_route=alert.target_route,
            attacker_ip=alert.attacker_ip,
            user_agent=alert.user_agent,
            headers=alert.headers,
            timestamp=alert.timestamp
        )
        db.session.add(alert_db)
        db.session.commit()
        alert.id = alert_db.id
        return alert

    def find_all(self) -> List[Alert]:
        alerts_db = AlertDB.query.all()
        return [
            Alert(
                id=a.id,
                target_route=a.target_route,
                attacker_ip=a.attacker_ip,
                user_agent=a.user_agent,
                headers=a.headers,
                timestamp=a.timestamp
            ) for a in alerts_db
        ]

class SQLAlchemyHoneytokenRepository(HoneytokenRepository):
    def save(self, honeytoken: Honeytoken) -> Honeytoken:
        honeytoken_db = HoneytokenDB(
            route=honeytoken.route,
            description=honeytoken.description,
            is_active=honeytoken.is_active,
            response_type=honeytoken.response_type
        )
        db.session.add(honeytoken_db)
        db.session.commit()
        honeytoken.id = honeytoken_db.id
        return honeytoken

    def find_all(self) -> List[Honeytoken]:
        honeytokens_db = HoneytokenDB.query.all()
        return [
            Honeytoken(
                id=h.id,
                route=h.route,
                description=h.description,
                is_active=h.is_active,
                response_type=h.response_type
            ) for h in honeytokens_db
        ]

    def find_by_route(self, route: str) -> Optional[Honeytoken]:
        h = HoneytokenDB.query.filter_by(route=route).first()
        if not h:
            return None
        return Honeytoken(
            id=h.id,
            route=h.route,
            description=h.description,
            is_active=h.is_active,
            response_type=h.response_type
        )

class SQLAlchemyBannedIPRepository(BannedIPRepository):
    def save(self, banned_ip: BannedIP) -> BannedIP:
        banned_db = BannedIPDB(
            ip=banned_ip.ip,
            reason=banned_ip.reason,
            banned_at=banned_ip.banned_at
        )
        db.session.merge(banned_db)
        db.session.commit()
        banned_ip.id = banned_db.id
        return banned_ip

    def find_by_ip(self, ip: str) -> Optional[BannedIP]:
        b = BannedIPDB.query.filter_by(ip=ip).first()
        if not b:
            return None
        return BannedIP(
            id=b.id,
            ip=b.ip,
            reason=b.reason,
            banned_at=b.banned_at
        )
