import datetime
import os
from typing import Optional, List

from core.services.analytics import AnalyticsServiceABC, ApiAnalyticsService
from core.services.api_client import ApiClientABC
from core.services.cache import EventCache, CacheABC
from core.services.google_calendar import GoogleCalendarAdapter
from core.storage.redis_connection import redis_client
from core.storage.storage import StorageABC, RedisStorage
from core.use_cases.events_managment.adt.interactor import AdtInteractor
from core.use_cases.events_managment.interactor import EventInteractor
from core.use_cases.events_managment.scheme import Event


def init_events_management(
    api_client: ApiClientABC = None,
    analytics_client: AnalyticsServiceABC = None,
) -> AdtInteractor:
    analytics = (
        analytics_client or
        ApiAnalyticsService(RedisStorage("analytics", redis_client))
    )
    if not api_client:
        api_client = GoogleCalendarAdapter(
            credentials_file=os.getenv("GOOGLE_CREDENTIALS_FILE"),
            token_file=os.getenv("GOOGLE_TOKEN_FILE"),
        )
    return EventInteractor(
        api_client=api_client,
        analytics=analytics,
    )


def init_cache_storage(storage: StorageABC = None) -> CacheABC:
    storage = storage or RedisStorage("cache", redis_client)
    return EventCache(storage=storage)


async def bl_create_event(
    interactor: AdtInteractor,
    title: str,
    start_datetime: datetime.datetime,
    description: Optional[str] = None,
) -> Event:
    return await interactor.create_event(
        title=title,
        start_datetime=start_datetime,
        description=description,
    )


async def bl_delete_event(
    interactor: AdtInteractor,
    item_id: str,
) -> bool:
    return await interactor.delete_event(item_id)


async def bl_list_events(
    interactor: AdtInteractor,
    for_day: datetime.date,
) -> List[Event]:
    return await interactor.list_events(for_day)
