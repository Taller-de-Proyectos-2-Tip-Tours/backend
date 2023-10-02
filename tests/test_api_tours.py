import os

os.environ["TESTING"] = "True"

from api.tours_api import ToursSchema
import pytest
from marshmallow import ValidationError

def test_complete_tour():
    request = {
        "name": "Nuevo paseo creado en api deployada",
        "duration": "23:30",
        "description": "alto paseo",
        "minParticipants": 8,
        "maxParticipants": 10,
        "city": "Córdoba",
        "considerations": "Hay que caminar mucho",
        "lenguage": "Español",
        "meetingPoint": "Obelisco",
        "dates": ["2023-07-09T14:00"],
        "mainImage": "mockImage",
        "otherImages": ["mockImage2", "mockImage3", "mockImage4"],
        "lat": 1.2,
        "lon": 1.4,
        "guide": {
            "name": "Juan Perez",
            "email": "mail@mail.com"
        }
    }
    schema = ToursSchema()
    try:
        schema.load(request)
    except ValidationError as err:
        pytest.fail(err)
