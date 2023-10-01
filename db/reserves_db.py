import pymongo
import sys
from bson.json_util import dumps
import os

class ReservesCollection:
  _reserves = None

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
      self._reserves = db["reserves"]

  def insert_reserve(self, reserve):
    self._reserves.insert_one(reserve)

  def get_reserves_for_tour(self, tourId):
    data = self._reserves.find({"tourId": tourId})
    return dumps(data)
  
  def get_reserves_for_traveler(self, email):
    data = self._reserves.find({"traveler.email": email})
    return dumps(data)