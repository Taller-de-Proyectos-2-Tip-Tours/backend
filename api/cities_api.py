from flask import Blueprint
import json
from db.cities_db import CitiesCollection

cities = Blueprint('cities',__name__)
cities_collection = CitiesCollection()

@cities.route("/cities", methods=['GET'])
def get_tours():
    return json.loads(cities_collection.get_all_cities()), 200