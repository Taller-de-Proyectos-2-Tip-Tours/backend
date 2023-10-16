import os
from flask import Flask
os.environ["TESTING"] = "True"

from api.reviews_api import ReviewSchema, reviews
import pytest
from marshmallow import ValidationError

def test_complete_review():
    request = {
        "stars": 4.5,
        "comment": "Una inmersión fascinante en el vibrante arte callejero de Buenos Aires. Guías apasionados y obras impactantes. Imperdible.",
        "userEmail": "diego@mail.com",
        "userName": "Diego",
        "tourId": "651b1609031d7156530b2206",
        "date": "2023-10-16T20:02:32",
        "state": "active"
    }
    schema = ReviewSchema()
    try:
        schema.load(request)
    except ValidationError as err:
        pytest.fail(err)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(reviews)
    return app

def test_delete_review(app):
    client = app.test_client()
    response = client.delete('/reviews/652dc7828b3175f3026ee2fd')
    assert response.status_code == 200