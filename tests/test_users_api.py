import os
from flask import Flask
os.environ["TESTING"] = "True"

from api.users_api import users
import pytest

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(users)
    return app

def test_login(app):
    client = app.test_client()
    request = {
        "userEmail": "user@mail.com",
        "deviceToken": "123567"
    }
    response = client.post('/users/login', json=request)
    assert response.status_code == 200