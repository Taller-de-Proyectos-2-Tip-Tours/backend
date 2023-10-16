from flask import request, jsonify, Blueprint
import json
from db.reviews_db import ReviewsCollection
from marshmallow import Schema, fields, ValidationError, validates_schema
from db.tours_db import ToursCollection
from bson.objectid import ObjectId
from datetime import datetime
import pytz

reviews = Blueprint('reviews',__name__)
reviews_collection = ReviewsCollection()
tours_collection = ToursCollection()

class ReviewSchema(Schema):
  userEmail = fields.String(required=True)
  userName = fields.String(required=True)
  comment = fields.String(required=True)
  stars = fields.Integer(required=True)
  tourId = fields.String(required=True)
  date = fields.String(required=True)
  state = fields.String(required=True)

  @validates_schema
  def validate_comment(self, data, **kwargs):
    if len(data['comment']) > 200:
      raise ValidationError("El comentario de la review no puede contener más de 200 caracteres")
    
  @validates_schema
  def validate_stars(self, data, **kwargs):
    if data['stars'] > 5 or data['stars'] < 1:
      raise ValidationError("La valoración de la review debe tener entre 1 y 5 estrellas")
  
  @validates_schema
  def validate_tourId_people(self, data, **kwargs):
    try:
      ObjectId(data['tourId'])
    except:
      raise ValidationError("El tour seleccionado no existe.")
    tour = json.loads(tours_collection.get_tour_by_id(data['tourId']))
    if tour is None:
      raise ValidationError("El tour seleccionado no existe.")

@reviews.route("/reviews/<tourId>", methods=['GET'])
def get_reviews(tourId):
    return json.loads(reviews_collection.get_reviews_for_tour(tourId, request.args.get('state'))), 200

@reviews.route("/reviews/<tourId>", methods=['POST'])
def post_review(tourId):
    review = request.json
    schema = ReviewSchema()
    review["tourId"] = tourId
    ar_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    current_time_ar = datetime.now(ar_timezone)
    review["date"] = current_time_ar.strftime('%Y-%m-%dT%H:%M:%S')
    review["state"] = "active"
    try:
        result = schema.load(review)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    reviews_collection.insert_review(review)
    return {"success": "La review fue creada con éxito."}, 201

@reviews.route("/reviews/<reviewId>", methods=['DELETE'])
def delete_review(reviewId):
    try:
      review = json.loads(reviews_collection.get_review_by_id(reviewId))
      if review is None:
        return {
            "error": "La review no existe." 
          }, 404
      reviews_collection.update_review_state(reviewId, "inactive")
    except Exception as err:
      return {"error": str(err)}, 400
    return {"success": "La review fue desactivada con éxito."}, 200