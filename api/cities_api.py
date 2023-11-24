from flask import Blueprint
import json
from db.cities_db import CitiesCollection
import os
from utilities.authentication import token_required, app_token

cities = Blueprint('cities',__name__)
cities_collection = CitiesCollection()

@cities.route("/cities", methods=['GET'])
@app_token(expected_tokens=[os.getenv("backofficeToken"), os.getenv("webAppToken"), os.getenv("mobileAppToken")])
@token_required
def get_tours():
    return json.loads(cities_collection.get_all_cities()), 200