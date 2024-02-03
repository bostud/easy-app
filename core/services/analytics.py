import uuid
from abc import ABC, abstractmethod

from core.storage.storage import StorageABC


class AnalyticsServiceABC(ABC):
    @abstractmethod
    async def save_data(self, **kwargs):
        ...


class ApiAnalyticsService(AnalyticsServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage
        self._prefix = "analytics"

    async def save_data(self, **kwargs):
        call_id = kwargs.get("call_id") or str(uuid.uuid4())
        key = f"{self._prefix}:{call_id}"
        await self.storage.save(key, kwargs)
