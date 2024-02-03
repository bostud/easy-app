import datetime
from typing import Optional, List

from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse

from api.bl.events import (
    init_events_management,
    bl_create_event,
    bl_list_events,
    bl_delete_event,
    init_cache_storage,
)
from api.v1.utils import prepare_item_response
from api.json_scheme.scheme import CreateItem, Item

router = APIRouter(
    prefix='/calendar',
    tags=['json'],
    default_response_class=JSONResponse,
)


@router.get('/')
async def get_events_list(
    for_day: Optional[datetime.date] = None,
) -> Optional[List[Item]]:
    if not for_day:
        for_day = datetime.date.today()
    interactor = init_events_management()
    cache_storage = init_cache_storage()
    data = await cache_storage.get(for_day)
    if data:
        return [prepare_item_response(d) for d in data]

    data = await bl_list_events(interactor, for_day)
    await cache_storage.set(for_day, data)
    return [prepare_item_response(d) for d in data] if data else []


@router.post('/')
async def create_event(
    item: CreateItem,
) -> Item:
    interactor = init_events_management()
    _item = await bl_create_event(
        interactor=interactor,
        title=item.title,
        description=item.description,
        start_datetime=item.start_datetime,
    )
    return prepare_item_response(_item)


@router.delete('/{item_id}/')
async def delete_item(
    item_id: str,
) -> Response:
    interactor = init_events_management()
    _is_deleted = await bl_delete_event(interactor, item_id)
    message = 'OK' if _is_deleted else 'Item: %s - Not found' % item_id
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': message}
    )
