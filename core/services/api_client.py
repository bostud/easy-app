import datetime
from abc import ABC, abstractmethod
from typing import List


class ApiClientABC(ABC):
    @abstractmethod
    def create_event(self, event_details: dict) -> dict:
        ...

    @abstractmethod
    def get_events(self, for_date: datetime.date) -> List[dict]:
        ...

    @abstractmethod
    def delete_event(self, event_id: str) -> dict:
        ...
