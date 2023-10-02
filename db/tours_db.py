import pymongo
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
import os

class ToursCollection:
  _tours = None

  def __init__(self) -> None:
      try:
        client = pymongo.MongoClient("mongodb+srv://tdp2fiuba:GeroSantiVeroDiego@tdp2-db.5ruzja7.mongodb.net/?retryWrites=true&w=majority")
      # return a friendly error if a URI error is thrown 
      except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)
      # use a database named "myDatabase"
      if os.environ["TESTING"] == "True":
        db = client.mockDatabase
      else:
        db = client.myDatabase
      self._tours = db["tours"]

  def get_all_tours(self, name = None, city = None, guideEmail = None, dateState = None):
    pipeline = []

    # Match stage to filter tours based on other criteria
    match_stage = {}
    if name:
        match_stage["name"] = {"$regex": name}
    if city:
        match_stage["city"] = city
    if guideEmail:
        match_stage["guide.email"] = guideEmail
    pipeline.append({"$match": match_stage})

    # Unwind the "dates" array to work with individual dates
    pipeline.append({"$unwind": "$dates"})

    # Match stage to filter dates with the specified state
    if dateState:
        date_match_stage = {"dates.state": dateState}
        pipeline.append({"$match": date_match_stage})

    # Group the results by tour ID and reconstruct the "dates" array
    group_stage = {
        "_id": "$_id",
        "name": {"$first": "$name"},
        "city": {"$first": "$city"},
        "guide": {"$first": "$guide"},
        "dates": {"$push": "$dates"}
    }
    pipeline.append({"$group": group_stage})

    data = self._tours.aggregate(pipeline)

    return dumps(data)
  
  def insert_tour(self, tour):
    self._tours.insert_one(tour)

  def remove_tour(self, id):
    self._tours.delete_one({"name": id})

  def insert_many(self, tours):
    self._tours.insert_many(tours)

  def drop_collection(self):
    self._tours.drop()

  def get_tour_by_id(self, tourId):
    data = self._tours.find({"_id" : ObjectId(tourId)}, {"maxParticipants": 1})
    return dumps(data)