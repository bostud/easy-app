import datetime
from typing import Optional, List

from core.services.analytics import AnalyticsServiceABC
from core.services.api_client import ApiClientABC
from core.use_cases.events_managment.adt.interactor import AdtInteractor
from core.use_cases.events_managment.scheme import Event


def prepare_event(data: dict) -> Event:
    yield Event(
        item_id=data.get("item_id"),
        title=data.get("title"),
        description=data.get("description"),
        start_datetime=data.get("start_datetime"),
    )


class EventInteractor(AdtInteractor):
    def __init__(
        self,
        api_client: ApiClientABC,
        analytics: AnalyticsServiceABC,
    ):
        self.api_client = api_client
        self.analytics = analytics

    async def create_event(
        self,
        title: str,
        start_datetime: datetime.datetime,
        description: Optional[str] = None,
    ) -> Event:
        event_details = {
            "title": title,
            "description": description,
            "start_datetime": start_datetime,
        }
        data = self.api_client.create_event(event_details)
        await self.analytics.save_data(event=data, method="create")
        return prepare_event(data)

    async def delete_event(self, item_id: str) -> bool:
        data = self.api_client.delete_event(item_id)
        data["item_id"] = item_id
        await self.analytics.save_data(**data, method="delete")
        return True if data.get("status") == "Ok" else False

    async def list_events(
        self,
        for_date: datetime.date,
    ) -> List[Event]:
        data = self.api_client.get_events(
            for_date=for_date,
        )
        await self.analytics.save_data(**{"events": data}, method="events")
        return [prepare_event(d) for d in data]
