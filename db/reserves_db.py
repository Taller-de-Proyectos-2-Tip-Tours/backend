import pymongo
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
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
    data = self._reserves.insert_one(reserve)
    return dumps(data.inserted_id)

  def get_reserves_for_tour(self, tourId):
    data = self._reserves.find({"tourId": tourId}, {"notified": 0})
    return dumps(data)
  
  def get_reserves_for_traveler(self, email):
    data = self._reserves.find({"traveler.email": email}, {"notified": 0})
    return dumps(data)
  
  def get_reserves_for_traveler_tour(self, email, tourId):
    data = self._reserves.find({"traveler.email": email, "tourId": tourId, "state": "abierto"}, {"notified": 0})
    return dumps(data)
  
  def get_reserve_by_id(self, reserveId):
    data = self._reserves.find_one({"_id" : ObjectId(reserveId)}, {"notified": 0})
    return dumps(data)
  
  def change_reserve_state(self, reserveId, state):
    self._reserves.update_one({"_id" : ObjectId(reserveId)}, {"$set": {"state": state}})

  def drop_collection(self):
    self._reserves.drop()

  def get_reserves_coming_soon(self, date):
    data = self._reserves.find({"date": {"$lt": date}, "notified": {"$exists": False}, "state": "abierto"}, {"notified": 0})
    return dumps(data)

  def mark_notified(self, reserveId):
    self._reserves.update_one({"_id" : ObjectId(reserveId)}, {"$set": {"notified": 1}})

  def get_active_users_by_date(self, date):
    data = self._reserves.find({"date": {"$lte": date}, "state": "finalizado"}, {"traveler": 1})
    unique_emails = set(reserve["traveler"]["email"] for reserve in data)
    return len(unique_emails)
  
  def get_reserves_between_dates(self, startDate, endDate):
    data = self._reserves.find({"date": {"$lte": endDate, "$gte": startDate}}, {"tourId": 1})
    return dumps(data)