import os

os.environ["TESTING"] = "True"

from api.reserves_api import ReservesSchema
import pytest
from marshmallow import ValidationError

def test_complete_reserve():
    request = {
        "tourId": "651b1609031d7156530b2206",
        "dateId": "1234",
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