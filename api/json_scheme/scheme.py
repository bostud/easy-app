import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class CreateItem(BaseModel):
    class Config:
        extra = Extra.ignore

    title: str = Field(..., max_length=50)
    start_datetime: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
    )
    description: Optional[str] = Field(None, max_length=250)


class Item(CreateItem):
    item_id: str
