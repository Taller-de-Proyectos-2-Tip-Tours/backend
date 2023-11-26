import pymongo
import sys
import os
from bson.json_util import dumps
from bson.objectid import ObjectId

class ReviewsCollection:
  _reviews = None

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
      self._reviews = db["reviews"]

  def get_all_reviews(self):
    data = list(self._reviews.find())
    return dumps(data)
  
  def get_reviews_for_tour(self, tourId, state = None):
    if state:
      data = list(self._reviews.find({"tourId": tourId, "state": state}))
    else:  
      data = list(self._reviews.find({"tourId": tourId}))
    return dumps(data)
  
  def insert_review(self, review):
    self._reviews.insert_one(review)

  def drop_collection(self):
    self._reviews.drop()

  def get_review_by_id(self, reviewId):
    data = self._reviews.find_one({"_id" : ObjectId(reviewId)})
    return dumps(data)
  
  def update_review_state(self, reviewId, state):
    self._reviews.update_one({"_id" : ObjectId(reviewId)}, {"$set": {"state": state}})
