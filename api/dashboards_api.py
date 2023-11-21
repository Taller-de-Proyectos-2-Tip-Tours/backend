from db.reserves_db import ReservesCollection
from utilities.authentication import token_required
from flask import request, Blueprint
from datetime import datetime, timedelta
from db.tours_db import ToursCollection
from collections import Counter
import json

dashboards = Blueprint('dashboards',__name__)
reserves_collection = ReservesCollection()
tours_collection = ToursCollection()

def get_travelers_evolution(start_date, end_date):
  start_date = datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")
  current_date = start_date
  travelers = []
  while current_date <= end_date:
    current_date_str = current_date.strftime("%Y-%m-%d")
    body = {
      "travelers": reserves_collection.get_active_users_by_date(current_date_str),
      "date": current_date_str
    }
    travelers.append(body)
    current_date += timedelta(days=1)
  return travelers

def get_guides_evolution(start_date, end_date):
  start_date = datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")
  current_date = start_date
  guides = []
  while current_date <= end_date:
    current_date_str = current_date.strftime("%Y-%m-%d")
    body = {
      "guides": tours_collection.get_active_users_by_date(current_date_str),
      "date": current_date_str
    }
    guides.append(body)
    current_date += timedelta(days=1)
  return guides

@dashboards.route("/dashboards/evolution", methods=['GET'])
@token_required
def get_evolution():
  response = {
    "travelers": get_travelers_evolution(request.args.get('start_date'),
                                         request.args.get('end_date')),
    "guides": get_guides_evolution(request.args.get('start_date'),
                                   request.args.get('end_date'))
  }
  return response, 200

@dashboards.route("/dashboards/tourstopten", methods=['GET'])
@token_required
def get_tours_top_ten():
  request.args.get('start_date')
  request.args.get('end_date')
  reserves = json.loads(reserves_collection.get_reserves_between_dates(request.args.get('start_date'), 
                                                                       request.args.get('end_date')))
  tour_ids = [reserve["tourId"] for reserve in reserves]
  tour_id_counts = Counter(tour_ids)
  sorted_tour_id_counts = dict(sorted(tour_id_counts.items(), key=lambda x: x[1], reverse=True))
  top_10_tour_id_counts = {tour_id: count for tour_id, count in list(sorted_tour_id_counts.items())[:10]}
  response = []
  for tour_id, count in top_10_tour_id_counts.items():
    tour = json.loads(tours_collection.get_tour_by_id(tour_id, {'name': 1}))
    response.append({
      "tour": tour['name'],
      "reserves": count
    })
  print(tour_id_counts)
  result_json = [{"tour": tour_id, "reserves": count} for tour_id, count in tour_id_counts.items()]
  return result_json, 200
