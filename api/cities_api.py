from flask import Blueprint
import json
from db.cities_db import CitiesCollection
from utilities.authentication import token_required

cities = Blueprint('cities',__name__)
cities_collection = CitiesCollection()

@cities.route("/cities", methods=['GET'])
@token_required
def get_tours():
    return json.loads(cities_collection.get_all_cities()), 200