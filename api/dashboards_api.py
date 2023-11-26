from db.reserves_db import ReservesCollection
from utilities.authentication import token_required, app_token
from flask import request, Blueprint
from datetime import datetime, timedelta
from db.tours_db import ToursCollection
from db.reviews_db import ReviewsCollection
from collections import Counter
import json
import os
import scipy.stats as st
from collections import defaultdict
import math

dashboards = Blueprint('dashboards',__name__)
reserves_collection = ReservesCollection()
tours_collection = ToursCollection()
reviews_collection = ReviewsCollection()

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

def bayesian_rating(n, confidence=0.95):
    if sum(n)==0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        first_part += (k+1)*(n[k]+1)/(N+K)
        second_part += (k+1)*(k+1)*(n[k]+1)/(N+K)
    score = first_part - z * math.sqrt((second_part - first_part*first_part)/(N+K+1))
    return score

@dashboards.route("/dashboards/evolution", methods=['GET'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken")])
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
@app_token(expected_tokens=[os.getenv("backofficeToken")])
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

@dashboards.route("/dashboards/besttours", methods=['GET'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken")])
def get_best_rated_tours():
  reviews = json.loads(reviews_collection.get_all_reviews())
  tour_reviews = defaultdict(list)
  for review in reviews:
    tour_reviews[review['tourId']].append(review['stars'])
  print(tour_reviews)
  tours = []
  for id, scores in tour_reviews.items():
    bayesian_avg = bayesian_rating(scores)
    tours.append({"id": id, "score": bayesian_avg})
  sorted_scores = sorted(tours, key=lambda x: x['score'], reverse=True)
  top_10_scores = sorted_scores[:10]
  response = []
  for scores in top_10_scores:
    tour = json.loads(tours_collection.get_tour_by_id(scores['id'], {'name': 1}))
    response.append({
      "tour": tour['name'],
      "score": scores["score"]
    })
  return response, 200

@dashboards.route("/dashboards/bannedratings", methods=['GET'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken")])
def get_banned_ratings():
  reviews = json.loads(reviews_collection.get_all_reviews())
  active_count = 0
  inactive_count = 0
  for review in reviews:
    if review["state"] == "active":
        active_count += 1
    elif review["state"] == "inactive":
        inactive_count += 1
  response = {
     "active": active_count,
     "inactive": inactive_count
  }
  return response, 200
