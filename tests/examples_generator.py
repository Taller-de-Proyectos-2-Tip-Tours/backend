from db.tours_db import ToursCollection
from db.tours_examples import examples

class ToursExampleGenerator:
  _tours_collection = ToursCollection()

  def generate_examples(self):
    self._tours_collection.insert_many(examples)

  def drop_tours(self):
    self._tours_collection.drop_collection()