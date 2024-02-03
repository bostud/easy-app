import json
from typing import Optional
from abc import ABC, abstractmethod

from redis.asyncio import Redis


class StorageABC(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[dict]:
        ...

    @abstractmethod
    async def save(self, key: str, value: dict, ttl: int = -1) -> None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...


class RedisStorage(StorageABC):
    def __init__(self, key_prefix: str, ar_client: Redis):
        self.ar_client = ar_client
        self.key_prefix = key_prefix

    def _prepare_key(self, key: str) -> str:
        return f"{self.key_prefix}:{key}"

    async def get(self, key: str) -> Optional[dict]:
        result = await self.ar_client.get(self._prepare_key(key))
        if not result:
            return None
        return json.loads(result)

    async def save(self, key: str, value: dict, ttl: int = -1) -> None:
        if ttl < 0:
            ttl = None

        return await self.ar_client.set(
            self._prepare_key(key),
            json.dumps(value or {}),
            ttl,
        )

    async def delete(self, key: str) -> None:
        return await self.ar_client.delete(self._prepare_key(key))
