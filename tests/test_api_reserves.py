import os
from flask import Flask
os.environ["TESTING"] = "True"

from api.reserves_api import ReservesSchema, reserves
import pytest
from marshmallow import ValidationError
from db.reserves_db import ReservesCollection

from db.reserves_db import ReservesCollection

def test_complete_reserve():
    request = {
        "tourId": "651b1609031d7156530b2206",
        "date": "1234",
        "traveler": {
            "name": "Diego",
            "email": "mail@mail.com"
        },
        "people": 1
    }
    schema = ReservesSchema()
    try:
        schema.load(request)
    except ValidationError as err:
        pytest.fail(err)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(reserves)
    return app

def test_reserve_using_api(app):
    request = {
        "tourId": "651b1609031d7156530b2206",
        "date": "2023-10-13T09:00:00",
        "traveler": {
            "name": "Diego",
            "email": "mail@mail.com"
        },
        "people": 1
    }
    client = app.test_client()
    response = client.post('/reserves', json=request)
    assert response.status_code == 201
    collection = ReservesCollection()
    response_data = response.get_json()
    collection.remove_reserve(response_data["$oid"])