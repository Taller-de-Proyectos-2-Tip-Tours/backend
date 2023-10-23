import pymongo
import sys
import json
from bson.json_util import dumps

class UsersCollection:
  _users = None

  def __init__(self) -> None:
      try:
        client = pymongo.MongoClient("mongodb+srv://tdp2fiuba:GeroSantiVeroDiego@tdp2-db.5ruzja7.mongodb.net/?retryWrites=true&w=majority")
      # return a friendly error if a URI error is thrown 
      except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)
      # use a database named "myDatabase"
      db = client.myDatabase
      self._users = db["users"]

  def get_device_token_by_email(self, userEmail):
    data = self._users.find_one({"userEmail": userEmail}, {"devicesTokens": 1})
    user = json.loads(dumps(data))
    if user is None:
      return []
    return user["devicesTokens"]
  