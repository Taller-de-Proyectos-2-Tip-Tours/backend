import pymongo
import sys
import json
import os
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
      if os.environ["TESTING"] == "True":
        db = client.mockDatabase
      else:
        db = client.myDatabase
      self._users = db["users"]

  def get_device_token_by_email(self, userEmail):
    data = self._users.find_one({"userEmail": userEmail}, {"devicesTokens": 1})
    user = json.loads(dumps(data))
    if user is None:
      return []
    return user["devicesTokens"]
  
  def get_user_by_email(self, userEmail):
    data = self._users.find_one({"userEmail": userEmail})
    return json.loads(dumps(data))
  
  def create_new_user(self, user):
    self._users.insert_one(user)

  def add_new_token(self, userEmail, token):
    data = self._users.find_one({"userEmail": userEmail})
    user = json.loads(dumps(data))
    self._users.update_one(
        {"_id": user["_id"]["$oid"]},
        {"$push": {"deviceToken": token}}
    )

  def drop_collection(self):
    self._users.drop()
  