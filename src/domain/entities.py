from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any

@dataclass
class Alert:
    """Domain model for a security alert triggered by a honeytoken"""
    target_route: str
    attacker_ip: str
    user_agent: str
    headers: Dict[str, str]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: int = None

@dataclass
class Honeytoken:
    """Domain model for a decoy honeytoken endpoint"""
    route: str
    description: str
    is_active: bool = True
    id: int = None
