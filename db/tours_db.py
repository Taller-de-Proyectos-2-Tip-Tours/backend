import pymongo
import sys
from bson.json_util import dumps
from bson.objectid import ObjectId
import os
import json

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

  def get_all_tours(self, name = None, city = None, guideEmail = None, state = None, dateState = None):
    pipeline = []

    # Match stage to filter tours based on other criteria
    match_stage = {}
    if name:
        match_stage["name"] = {"$regex": name}
    if city:
        match_stage["city"] = city
    if guideEmail:
        match_stage["guide.email"] = guideEmail
    if state:
        match_stage["state"] = state
    if dateState:
        match_stage["dates.state"] = dateState
    pipeline.append({"$match": match_stage})

    # Match stage to filter dates with the specified state
    if dateState:
        pipeline.append({
            "$addFields": {
                "dates": {
                    "$filter": {
                        "input": "$dates",
                        "as": "item",
                        "cond": {"$eq": ["$$item.state", dateState]}
                    }
                }
            }
        })

    # Match stage to filter out tours with empty dates array
    pipeline.append({"$match": {"dates": {"$ne": []}}})

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

  def get_tour_by_id(self, tourId, fields = {}):
    data = self._tours.find_one({"_id" : ObjectId(tourId)}, fields)
    return dumps(data)
  
  def update_tour_dates(self, dates, tourId):
    self._tours.update_one({"_id" : ObjectId(tourId)}, {"$set": {"dates": dates}})

  def cancel_tour_date(self, tourId, date):
    tour = json.loads(self.get_tour_by_id(tourId, {"dates": 1}))
    if tour is None:
      raise Exception("El tour no existe.")
    new_dates = []
    canceled_date = False
    for tour_date in tour["dates"]:
      if date == tour_date["date"]:
        canceled_date = True
        new_dates.append({
          "date": tour_date["date"],
          "state": "cancelado",
          "people": tour_date["people"]
        })
      else:
        new_dates.append(tour_date)
    if not canceled_date:
      raise Exception("La fecha seleccionada no existe.")
    self._tours.update_one({"_id" : ObjectId(tourId)}, {"$set": {"dates": new_dates}})

  def cancel_reserve_for_tour(self, tourId, date, people):
    tour = json.loads(self.get_tour_by_id(tourId, {"dates": 1}))
    if tour is None:
      raise Exception("El tour no existe.")
    new_dates = []
    canceled_date = False
    for tour_date in tour["dates"]:
      if date == tour_date["date"]:
        canceled_date = True
        new_sate = tour_date["state"]
        if new_sate == "cerrado":
          new_sate = "abierto"
        new_dates.append({
          "date": tour_date["date"],
          "state": new_sate,
          "people": tour_date["people"] - people
        })
      else:
        new_dates.append(tour_date)
    if canceled_date == False:
      raise Exception("La fecha seleccionada no existe.")
    self._tours.update_one({"_id" : ObjectId(tourId)}, {"$set": {"dates": new_dates}})

  def update_tour(self, tourId, updatedTour):
    tour = json.loads(self.get_tour_by_id(tourId, {}))
    if tour is None:
      raise Exception("El tour no existe")
    self._tours.update_one({"_id" : ObjectId(tourId)}, {"$set": updatedTour})

  def get_old_dates(self, date):
    data = self._tours.find(
      {
        "dates": {
          "$elemMatch": {
              "date": {"$lt": date},
              "state": "abierto"
          }
        }
      },
      {"dates": 1}
    )
    return dumps(data)
    
  def get_active_users_by_date(self, date):
    data = self._tours.find({"dates.state": "finalizado", "dates.date": {"$lte": date}}, {"guide": 1})
    unique_emails = set(tour["guide"]["email"] for tour in data)
    return len(unique_emails)