import pymongo
import sys
from data.tours_examples import examples
from bson.json_util import dumps

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
      db = client.myDatabase
      self._tours = db["tours"]


  def create_tours_collection(self, with_examples):
    tours = self.db["tours"]
    if with_examples:
      tours.insert_many(examples)

  def get_all_tours(self):
    data = self._tours.find()
    return dumps(data)