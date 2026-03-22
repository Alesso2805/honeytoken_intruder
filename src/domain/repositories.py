from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Honeytoken, Alert

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
