import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    item_id: str
    title: str
    start_datetime: datetime.datetime
    description: Optional[str] = None
