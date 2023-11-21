import os
from flask import Flask
os.environ["TESTING"] = "True"

from api.cities_api import cities
import pytest

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(cities)
    return app

def test_delete_review(app):
    client = app.test_client()
    response = client.get('/cities')
    assert response.status_code == 200