import datetime
from abc import ABC, abstractmethod
from typing import Optional, List

from core.use_cases.events_managment.scheme import Event


class AdtInteractor(ABC):
    @abstractmethod
    async def create_event(
        self,
        title: str,
        start_datetime: datetime.datetime,
        description: Optional[str] = None,
    ) -> Event:
        ...

    @abstractmethod
    async def delete_event(self, item_id: str) -> bool:
        ...

    @abstractmethod
    async def list_events(
        self,
        for_date: datetime.date,
    ) -> List[Event]:
        ...
