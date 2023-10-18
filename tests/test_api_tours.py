import os
from flask import Flask
os.environ["TESTING"] = "True"

from api.tours_api import ToursSchema, tours
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
        "stops": [
            {
                "lat": 1.3,
                "lon": 1.2,
                "tag": "inicio"
            },
            {
                "lat": 1.3,
                "lon": 1.3,
                "tag": "fin"
            }
        ],
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

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(tours)
    return app

def test_cancel_tour_date(app):
    client = app.test_client()
    response = client.put('/tours/cancel?tourId=651b1609031d7156530b2206&date=2024-10-15T10:30:00')
    assert response.status_code == 201

def test_update_state_tour(app):
    client = app.test_client()
    response = client.put('/tours/651b1609031d7156530b2206?state=borrador')
    assert response.status_code == 201