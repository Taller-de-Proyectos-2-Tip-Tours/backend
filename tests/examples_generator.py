from db.tours_db import ToursCollection
from db.reserves_db import ReservesCollection
from db.reviews_db import ReviewsCollection
from db.tours_examples import examples

class ToursExampleGenerator:
  _tours_collection = ToursCollection()
  _reserves_collection = ReservesCollection()
  _reviews_collection = ReviewsCollection()

  def generate_examples(self):
    self._tours_collection.insert_many(examples)

  def drop_reserves(self):
    self._reserves_collection.drop_collection()

  def drop_tours(self):
    self._tours_collection.drop_collection()

  def drop_reviews(self):
    self._reviews_collection.drop_collection()