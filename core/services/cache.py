import datetime
from abc import ABC, abstractmethod
from typing import Any

from core.storage.storage import StorageABC


class CacheABC(ABC):
    @abstractmethod
    async def get(
        self,
        for_date: datetime.date,
    ) -> Any:
        ...

    @abstractmethod
    async def set(
        self,
        for_date: datetime.date,
        data: Any,
    ) -> bool:
        ...


class EventCache(CacheABC):
    def __init__(self, storage: StorageABC, ttl: int = 24 * 3600) -> None:
        self._storage = storage
        self._ttl = ttl

    @staticmethod
    def generate_key(for_date: datetime.date) -> str:
        return (
            f"eventdata:{for_date.year}-{for_date.month}-{for_date.day}"
        )

    async def get(
        self,
        for_date: datetime.date,
    ) -> Any:
        key = self.generate_key(for_date)
        return await self._storage.get(key)

    async def set(
        self,
        for_date: datetime.date,
        data: Any,
    ) -> bool:
        key = self.generate_key(for_date)
        await self._storage.save(key, data, ttl=self._ttl)
        return True
