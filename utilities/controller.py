from datetime import datetime
from db.tours_db import ToursCollection
import json

class Controller:
  _tours_collection = ToursCollection()
  
  def end_tours(self):
    print("Executing end tours process")
    today = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    tours = json.loads(self._tours_collection.get_old_dates(today))
    for tour in tours:
      new_dates = []
      for date in tour["dates"]:
        if date["date"] < today:
          new_dates.append({"date": date["date"], "people": date["people"], "state": "finalizado"})
        else:
          new_dates.append(date)
      self._tours_collection.update_tour_dates(new_dates, tour["_id"]["$oid"])
