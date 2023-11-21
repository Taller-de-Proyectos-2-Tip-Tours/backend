from db.reserves_db import ReservesCollection
from utilities.authentication import token_required
from flask import request, Blueprint
from datetime import datetime, timedelta
from db.tours_db import ToursCollection

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