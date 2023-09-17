import pymongo
import sys
from bson.json_util import dumps
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

  def get_all_tours(self):
    data = self._tours.find()
    return dumps(data)
  
  def insert_tour(self, tour):
    self._tours.insert_one(tour)

  def remove_tour(self, id):
    self._tours.delete_one({"name": id})