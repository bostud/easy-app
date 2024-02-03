import datetime

from fastapi.testclient import TestClient
from start_app import app

client = TestClient(app)

today_now = datetime.datetime.now()
test_item_1 = {
    'title': 'Google Meet Test',
    'description': "Hi there - will meet u soon",
    "start_datetime": today_now,
}
test_item_2 = {
    'title': 'Google Meet Test 2',
    'description': "Bye there - will meet u on Monday",
    "start_datetime": today_now,
}
test_item_invalid = {
    'description': 'no title item'
}

test_item_invalid_2 = {
    'title': 'Invalid Body',
}

calendar_api_base = '/api/v1/calendar'
created_in_tests = []


def test_get_items():
    created_item_ids = []
    # create item 1
    resp_1 = client.post(calendar_api_base, json=test_item_1)
    assert resp_1.status_code == 200
    created_item_ids.append(resp_1.json()['item_id'])

    # create item 2
    resp_2 = client.post(calendar_api_base, json=test_item_2)
    assert resp_2.status_code == 200
    created_item_ids.append(resp_2.json()['item_id'])

    resp = client.get(calendar_api_base, params={"for_day": today_now.date()})
    assert resp.status_code == 200

    data = resp.json()
    items_ids = [i['item_id'] for i in data]
    for created_item_id in created_item_ids:
        assert created_item_id in items_ids

    created_in_tests.extend(created_item_ids)


def test_create_invalid():
    resp = client.post(calendar_api_base, json=test_item_invalid)
    assert resp.status_code == 422

    resp = client.post(calendar_api_base, json=test_item_invalid_2)
    assert resp.status_code == 422


def test_delete_item():
    resp = client.post(calendar_api_base, json=test_item_2)
    assert resp.status_code == 200

    item_data = resp.json()
    item_id = item_data['item_id']

    created_in_tests.append(item_id)

    for item_id in created_in_tests:
        resp = client.delete(calendar_api_base + '/' + str(item_id) + '/')
        assert resp.status_code == 200
        assert resp.json()['message'] == 'OK'
