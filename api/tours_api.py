from db.tours_db import ToursCollection
from db.cities_db import CitiesCollection
from flask import request, jsonify, Blueprint
import json
from marshmallow import Schema, fields, ValidationError, validates_schema
import time
from datetime import datetime, timedelta
from db.reserves_db import ReservesCollection
from db.reviews_db import ReviewsCollection
from utilities.authentication import token_required, app_token
from utilities.notificator import Notificator
import pytz
import os

tours = Blueprint('tours',__name__)
tours_collection = ToursCollection()
cities_collection = CitiesCollection()
reserves_collection = ReservesCollection()
reviews_collection = ReviewsCollection()
notificator = Notificator() 

lenguages = ["Español", "Inglés", "Portugués", "Alemán", "Francés", "Italiano"]

class GuideSchema(Schema):
  name = fields.String(required=True)
  email = fields.String(required=True)

class StopSchema(Schema):
  lat = fields.Float(required=True)
  lon = fields.Float(required=True)
  tag = fields.String()

class ToursSchema(Schema):
    guide = fields.Nested(GuideSchema, required=True)
    name = fields.String(required=True)
    duration = fields.String(required=True)
    description = fields.String(required=True)
    minParticipants = fields.Integer(required=True)
    maxParticipants = fields.Integer(required=True)
    city = fields.String(required=True)
    lenguage = fields.String(required=True)
    meetingPoint = fields.String(required=True)
    considerations = fields.String(required=True)
    dates = fields.List(fields.String(), required=True)
    mainImage = fields.String(required=True)
    otherImages = fields.List(fields.String(), required=True)
    stops = fields.List(fields.Nested(StopSchema), required=True)

    @validates_schema
    def validate_name(self, data, **kwargs):
      if len(data['name']) > 50:
        raise ValidationError("El nombre del paseo no puede contener más de 50 caracteres")
    
    @validates_schema
    def validate_description(self, data, **kwargs):
      if len(data['description']) > 200:
        raise ValidationError("La descripción del paseo no puede contener más de 200 caracteres")
      
    @validates_schema
    def validate_meeting_point(self, data, **kwargs):
      if len(data['meetingPoint']) > 200:
        raise ValidationError("Los puntos a tener en cuenta del paseo no puede contener más de 200 caracteres")

    @validates_schema
    def validate_participants(self, data, **kwargs):
      if data['minParticipants'] > data['maxParticipants']:
        raise ValidationError("El minimo de participantes debe ser menor al máximo")
      
    @validates_schema
    def validate_city(self, data, **kwargs):
      if cities_collection.get_city(data['city']) == None:
        raise ValidationError("La ciudad seleccionada no está disponible")
      
    @validates_schema
    def validate_duration(self, data, **kwargs):
        try:
            time.strptime(data["duration"], '%H:%M')
        except ValueError:
            raise ValidationError("La duración debe respetar el formato HH:MM")
        
    @validates_schema
    def validate_lenguage(self, data, **kwargs):
       if not data["lenguage"] in lenguages:
          raise ValidationError("El idioma seleccionado no está disponible")
       
    @validates_schema
    def validate_dates(self, data, **kwargs):
       for date in data["dates"]:
            try:
                formated_date = datetime.fromisoformat(date)
                if formated_date.hour == 0 and formated_date.minute == 0:
                   raise ValueError
            except:
                raise ValidationError("La fecha seleccionada no cumple con el formato ISO")
            
    @validates_schema
    def validate_other_images(self, data, **kwargs):
       length = len(data["otherImages"])
       if length < 1 or length > 4:
          raise ValidationError("El paseo debe contener entre 2 y 4 imagenes extras")

@tours.route("/tours", methods=['GET'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken"), os.getenv("webAppToken"), os.getenv("mobileAppToken")])
def get_tours():
    tours = json.loads(tours_collection.get_all_tours(request.args.get('name'), 
                                                     request.args.get('city'),
                                                     request.args.get('guideEmail'),
                                                     request.args.get('state'),
                                                     request.args.get('dateState')))
    for tour in tours:
      tour["dates"] = sorted(tour["dates"], key=lambda x: x["date"])
    return tours, 200

@tours.route("/tours", methods=['POST'])
@token_required
@app_token(expected_tokens=[os.getenv("webAppToken")])
def post_tours():
    tour = request.json
    schema = ToursSchema()
    try:
        result = schema.load(tour)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    # Send data back as JSON
    aux = []
    for date in tour["dates"]:
       aux.append({"date": date, "state": "abierto", "people": 0})
    tour["dates"] = aux
    tour["state"] = "borrador"
    tours_collection.insert_tour(tour)
    return {"success": "El paseo fue creado con éxito."}, 201

@tours.route("/tours/cancel", methods=['PUT'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken"), os.getenv("webAppToken")])
def cancel_tour_date():
    tourId = request.args.get('tourId')
    date = request.args.get('date')
    isAdmin = request.args.get('isAdmin', default='False')
    if (tourId is None) or (date is None):
       return {
          "error": "Debe enviar un tourId y date para cancelar." 
       }, 400
    argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
    tour_date = argentina_timezone.localize(datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"))
    time_difference = tour_date - datetime.now(argentina_timezone)
    if (abs(time_difference) < timedelta(hours=24)) and (isAdmin == "False"):
       return {
          "error": "No puede cancelar un paseo a menos de 24 horas del mismo." 
       }, 400
    try:
      tours_collection.cancel_tour_date(tourId, date)
      reserves = json.loads(reserves_collection.get_reserves_for_tour(tourId))
      tour_data = {
        "date": date,
        "state": "cancelado",
        "tourId": tourId
      }
      for reserve in reserves:
        if (reserve['date'] == date) and (reserve["state"] == "abierto") and ( not os.environ["TESTING"] == "True"):
          tour_data["reserveId"] = reserve['_id']['$oid']
          reserves_collection.change_reserve_state(reserve['_id']['$oid'], "cancelado")
          notificator.notify_cancelled_tour_date(reserve["traveler"]["email"], tour_data)
    except Exception as err:
      return {"error": str(err)}, 400
    return {
      "success": "La fecha fue cancelada con éxito.",
      "tourId": tourId,
      "date": date
    }, 201

@tours.route("/tours/<tourId>", methods=['GET'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken"), os.getenv("webAppToken"), os.getenv("mobileAppToken")])
def get_tour(tourId):
    try:
      tour = json.loads(tours_collection.get_tour_by_id(tourId))
      if tour is None:
        return {"error": "El tour no existe."}, 404
      tour["dates"] = sorted(tour["dates"], key=lambda x: x["date"])
      reviews = json.loads(reviews_collection.get_reviews_for_tour(tour["_id"]["$oid"], state="active"))
      if len(reviews) > 0:
        total_stars = sum(review["stars"] for review in reviews)
        average_stars = total_stars / len(reviews)
        tour["averageRating"] = average_stars
      else:
         tour["averageRating"] = 0
      return tour, 200
    except Exception as err:
      return {"error": str(err)}, 400
    
@tours.route("/tours/<tourId>", methods=['PUT'])
@token_required
@app_token(expected_tokens=[os.getenv("backofficeToken"), os.getenv("webAppToken")])
def update_tour_state(tourId):
    updated_tour = request.json
    if not (updated_tour.get("_id") is None):
      updated_tour.pop("_id")
    try:
      tours_collection.update_tour(tourId, updated_tour)
      reserves = json.loads(reserves_collection.get_reserves_for_tour(tourId))
      tour_data = {
        "tourId": tourId
      }
      for reserve in reserves:
        if (reserve["state"] == "abierto") and (not (os.environ["TESTING"] == "True")):
          tour_data["reserveId"] = reserve['_id']['$oid']
          tour_data["date"] = reserve['date']
          tour_data["state"] = reserve['state']
          print("Notifico")
          notificator.notify_modified_tour(reserve["traveler"]["email"], tour_data)
      return {"success": "El tour fue actualizado correctamente"}, 201
    except Exception as err:
       return {"error": str(err)}, 400
