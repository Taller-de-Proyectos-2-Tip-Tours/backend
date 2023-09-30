import os
import json

os.environ["TESTING"] = "True"

from db.reserves_db import ReservesCollection

#Get all tours devuelve los 2 tours presentes en la mockDB
def test_get_all_tours():
    collection = ReservesCollection()
    tours = json.loads(collection.get_reserves_for_tour("65035bf573ae9429e602edf1"))
    assert len(tours) == 1

#Insert tour agrega 1 tour presentes a la mockDB
#def test_insert_tour():
#    collection = ReservesCollection()
#    tours = json.loads(collection.get_reserves_for_tour("65035bf573ae9429e602edf1"))
#    assert len(tours) == 1
#    collection.insert_reserve({
#        "tourId": "65035bf573ae9429e602edf1"
#    })
#    tours = json.loads(collection.get_reserves_for_tour("65035bf573ae9429e602edf1"))
#    assert len(tours) == 2
#    collection.remove_reserve("Test tour 3")
