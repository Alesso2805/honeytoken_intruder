from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Honeytoken, Alert, BannedIP

class HoneytokenRepository(ABC):
    @abstractmethod
    def save(self, honeytoken: Honeytoken) -> Honeytoken:
        pass

    @abstractmethod
    def find_all(self) -> List[Honeytoken]:
        pass

    @abstractmethod
    def find_by_route(self, route: str) -> Optional[Honeytoken]:
        pass

class AlertRepository(ABC):
    @abstractmethod
    def save(self, alert: Alert) -> Alert:
        pass

    @abstractmethod
    def find_all(self) -> List[Alert]:
        pass

class BannedIPRepository(ABC):
    @abstractmethod
    def save(self, banned_ip: BannedIP) -> BannedIP:
        pass

    @abstractmethod
    def find_by_ip(self, ip: str) -> Optional[BannedIP]:
        pass
