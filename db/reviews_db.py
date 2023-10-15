import pymongo
import sys
import os
from bson.json_util import dumps

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

  def get_reviews_for_tour(self, tourId):
    data = list(self._reviews.find({"tourId": tourId}))
    return dumps(data)
  
  def insert_review(self, review):
    self._reviews.insert_one(review)