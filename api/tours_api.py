from db.tours_db import ToursCollection
from db.cities_db import CitiesCollection
from flask import request, jsonify, Blueprint
import json
from marshmallow import Schema, fields, ValidationError, validates_schema
import time
from datetime import datetime, timedelta
from db.reserves_db import ReservesCollection
from utilities.notificator import Notificator

tours = Blueprint('tours',__name__)
tours_collection = ToursCollection()
cities_collection = CitiesCollection()
reserves_collection = ReservesCollection()
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
def get_tours():
    return json.loads(tours_collection.get_all_tours(request.args.get('name'), 
                                                     request.args.get('city'),
                                                     request.args.get('guideEmail'),
                                                     request.args.get('state'),
                                                     request.args.get('dateState'))), 200

@tours.route("/tours", methods=['POST'])
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
def cancel_tour_date():
    tourId = request.args.get('tourId')
    date = request.args.get('date')
    if (tourId is None) or (date is None):
       return {
          "error": "Debe enviar un tourId y date para cancelar." 
       }, 400
    time_difference = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S") - datetime.now()
    if abs(time_difference) < timedelta(hours=24):
       return {
          "error": "No puede cancelar un paseo a menos de 24 horas del mismo." 
       }, 400
    try:
      tours_collection.cancel_tour_date(tourId, date)
      reserves = json.loads(reserves_collection.get_reserves_for_tour(tourId))
      unique_emails = set()
      tour_data = {
        "date": date,
        "state": "cancelado",
        "tourId": tourId
      }
      for reserve in reserves:
        if reserve['date'] == date:
          tour_data["reserveId"] = reserve['_id']['$oid']
          notificator.notify_cancelled_tour_date(reserve["traveler"]["email"], tour_data)
    except Exception as err:
      return {"error": str(err)}, 400
    return {
      "success": "La fecha fue cancelada con éxito.",
      "tourId": tourId,
      "date": date
    }, 201

@tours.route("/tours/<tourId>", methods=['GET'])
def get_tour(tourId):
    try:
      tour = json.loads(tours_collection.get_tour_by_id(tourId))
      if tour is None:
         return {"error": "El tour no existe."}, 404
      return tour, 200
    except Exception as err:
       return {"error": str(err)}, 400
    
@tours.route("/tours/<tourId>", methods=['PUT'])
def update_tour_state(tourId):
    updated_tour = request.json
    if not (updated_tour.get("_id") is None):
      updated_tour.pop("_id")
    try:
      tours_collection.update_tour(tourId, updated_tour)
      reserves = json.loads(reserves_collection.get_reserves_for_tour(tourId))
      unique_emails = set()
      for reserve in reserves:
        unique_emails.add(reserve["traveler"]["email"])
      for email in unique_emails:
        notificator.notify_modified_tour(email)
      return {"success": "El tour fue actualizado correctamente"}, 201
    except Exception as err:
       return {"error": str(err)}, 400
