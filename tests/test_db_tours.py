import os
import json

os.environ["TESTING"] = "True"

from db.tours_db import ToursCollection

#Get all tours devuelve los 2 tours presentes en la mockDB
def test_get_all_tours():
    collection = ToursCollection()
    tours = json.loads(collection.get_all_tours())
    assert len(tours) == 2

#Insert tour agrega 1 tour presentes a la mockDB
def test_insert_tour():
    collection = ToursCollection()
    tours = json.loads(collection.get_all_tours())
    assert len(tours) == 2
    collection.insert_tour({
        "name": "Test tour 3"
    })
    tours = json.loads(collection.get_all_tours())
    assert len(tours) == 3
    collection.remove_tour("Test tour 3")
