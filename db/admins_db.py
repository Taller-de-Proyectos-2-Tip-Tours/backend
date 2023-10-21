import pymongo
import sys
from bson.json_util import dumps

class AdminsCollection:
  _admins = None

  def __init__(self) -> None:
      try:
        client = pymongo.MongoClient("mongodb+srv://tdp2fiuba:GeroSantiVeroDiego@tdp2-db.5ruzja7.mongodb.net/?retryWrites=true&w=majority")
      # return a friendly error if a URI error is thrown 
      except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)
      # use a database named "myDatabase"
      db = client.myDatabase
      self._admins = db["admins"]

  def get_admin(self, username, password):
    data = self._admins.find_one({"username": username, "password": password})
    return dumps(data)