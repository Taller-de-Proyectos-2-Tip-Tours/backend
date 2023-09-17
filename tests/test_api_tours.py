import os

os.environ["TESTING"] = "True"

from api.tours import ToursSchema
import pytest
from marshmallow import ValidationError

def test_complete_tour():
    request = {
        "name": "Nuevo paseo creado con api",
        "duration": "10 hours",
        "description": "alto paseo",
        "minParticipants": 5,
        "maxParticipants": 5,
        "city": "Buenos Aires"
    }
    schema = ToursSchema()
    try:
        schema.load(request)
    except ValidationError as err:
        pytest.fail(err)
