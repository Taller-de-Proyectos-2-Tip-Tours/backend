import pymongo
import sys
import json
import os
from bson.json_util import dumps
from bson.objectid import ObjectId

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
    data = self._users.find_one({"userEmail": userEmail}, {"devicesTokens": 1, "_id": 1})
    user = json.loads(dumps(data))
    if user is None:
      return []
    return user
  
  def update_device_tokens_for_user(self, userId, updatedDeviceTokens):
    self._users.update_one({"_id" : ObjectId(userId)}, {"$set": {"devicesTokens": updatedDeviceTokens}})
  
  def get_user_by_email(self, userEmail):
    data = self._users.find_one({"userEmail": userEmail})
    return json.loads(dumps(data))
  
  def create_new_user(self, user):
    self._users.insert_one(user)

  def add_new_token(self, userEmail, token):
    data = self._users.find_one({"userEmail": userEmail})
    user = json.loads(dumps(data))
    new_tokens = []
    for existing_token in user["devicesTokens"]:
      new_tokens.append(existing_token)
    new_tokens.append(token)
    self._users.update_one(
        {"_id": ObjectId(user["_id"]["$oid"])},
        {"$push": {"devicesTokens": token}}
    )

  def drop_collection(self):
    self._users.drop()
  