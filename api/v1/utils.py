from api.json_scheme.scheme import Item
from core.use_cases.events_managment.scheme import Event


def prepare_item_response(item_data: Event) -> Item:
    return Item(
        item_id=item_data.item_id,
        title=item_data.title,
        description=item_data.description,
        start_datetime=item_data.start_datetime,
    )
