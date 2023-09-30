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

  def get_all_tours(self, name = None, city = None):
    if city and name:
      data = self._tours.find({"name" : {"$regex" : name}, "city": city})
    elif city:
      data = self._tours.find({"city": city})
    elif name:
      data = self._tours.find({"name" : {"$regex" : name}})
    else:
      data = self._tours.find({})
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