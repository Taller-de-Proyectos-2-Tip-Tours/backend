from flask import jsonify
import pymongo
import sys
from data.tours_examples import examples
from bson.json_util import dumps

class Database:
  _db = None

  def __init__(self) -> None:
      try:
        client = pymongo.MongoClient("mongodb+srv://tdp2fiuba:GeroSantiVeroDiego@tdp2-db.5ruzja7.mongodb.net/?retryWrites=true&w=majority")
      # return a friendly error if a URI error is thrown 
      except pymongo.errors.ConfigurationError:
        print("An Invalid URI host error was received. Is your Atlas host name correct in your connection string?")
        sys.exit(1)
      # use a database named "myDatabase"
      self.db = client.myDatabase


  def create_tours_collection(self, with_examples):
    tours = self.db["tours"]
    if with_examples:
      tours.insert_many(examples)

  def get_all_tours(self):
    data = self.db["tours"].find()
    return dumps(data)
  
  def drop_tours_collection(self):
    self.db["tours"].drop() 