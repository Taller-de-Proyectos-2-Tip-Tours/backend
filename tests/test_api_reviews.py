import os
from flask import Flask
os.environ["TESTING"] = "True"

from api.reviews_api import ReviewSchema
import pytest
from marshmallow import ValidationError

def test_complete_review():
    request = {
        "stars": 4.5,
        "comment": "Una inmersión fascinante en el vibrante arte callejero de Buenos Aires. Guías apasionados y obras impactantes. Imperdible.",
        "userEmail": "diego@mail.com",
        "userName": "Diego",
        "tourId": "651b1609031d7156530b2206"
    }
    schema = ReviewSchema()
    try:
        schema.load(request)
    except ValidationError as err:
        pytest.fail(err)