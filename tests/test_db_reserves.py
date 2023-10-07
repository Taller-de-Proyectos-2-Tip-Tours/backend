import os
import json

os.environ["TESTING"] = "True"

from db.reserves_db import ReservesCollection

#Get all tours devuelve los 2 tours presentes en la mockDB
def test_get_all_tours():
    collection = ReservesCollection()
    tours = json.loads(collection.get_reserves_for_tour("651b1609031d7156530b2206"))
    assert len(tours) == 1
