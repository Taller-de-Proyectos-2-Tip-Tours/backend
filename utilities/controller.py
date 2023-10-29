from datetime import datetime, timedelta
from db.tours_db import ToursCollection
from db.reserves_db import ReservesCollection
from utilities.notificator import Notificator
import json
import pytz

class Controller:
  _tours_collection = ToursCollection()
  _reserves_collection = ReservesCollection()
  _notificator = Notificator()
  
  def end_tours(self):
    argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    today = datetime.now(argentina_timezone).strftime("%Y-%m-%dT%H:%M:%S")
    tours = json.loads(self._tours_collection.get_old_dates(today))
    for tour in tours:
      new_dates = []
      for date in tour["dates"]:
        if date["date"] < today:
          new_dates.append({"date": date["date"], "people": date["people"], "state": "finalizado"})
        else:
          new_dates.append(date)
      self._tours_collection.update_tour_dates(new_dates, tour["_id"]["$oid"])
      reserves = json.loads(self._reserves_collection.get_reserves_for_tour(tour["_id"]["$oid"]))
      for reserve in reserves:
        if reserve["date"] < today:
          self._reserves_collection.change_reserve_state(reserve["_id"]["$oid"], "finalizado")

  def reserve_reminder(self):
    current_time = datetime.now()
    future_time = current_time + timedelta(hours=24)
    future_time_str = future_time.strftime("%Y-%m-%dT%H:%M:%S")
    reserves = json.loads(self._reserves_collection.get_reserves_coming_soon(future_time_str))
    for reserve in reserves:
      tour_data = {
        "date": reserve["date"],
        "state": reserve["state"],
        "tourId": reserve["tourId"],
        "reserveId": reserve['_id']['$oid']
      }
      self._notificator.notify_reserve_reminder(reserve["traveler"]["email"], tour_data)
      self._reserves_collection.mark_notified(reserve['_id']['$oid'])
