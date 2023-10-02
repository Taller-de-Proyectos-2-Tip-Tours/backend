from flask import request, jsonify, Blueprint
import json
from marshmallow import Schema, fields, ValidationError, validates_schema
from db.tours_db import ToursCollection
from bson.objectid import ObjectId
from db.reserves_db import ReservesCollection

reserves = Blueprint('reserves',__name__)
tours_collection = ToursCollection()
reserves_collection = ReservesCollection()

class TravelerSchema(Schema):
  name = fields.String(required=True)
  email = fields.String(required=True)

class ReservesSchema(Schema):
  tourId = fields.String(required=True)
  date = fields.String(required=True)
  traveler = fields.Nested(TravelerSchema, required=True)
  people = fields.Integer(required=True)

  @validates_schema
  def validate_people(self, data, **kwargs):
    if data['people'] <= 0:
      raise ValidationError("La cantidad de personas debe ser mayor a 0.")
    
  @validates_schema
  def validate_tourId_people(self, data, **kwargs):
    try:
        ObjectId(data['tourId'])
    except:
      raise ValidationError("El tour seleccionado no existe.")
    tour = json.loads(tours_collection.get_tour_by_id(data['tourId']))
    if len(tour) == 0:
      raise ValidationError("El tour seleccionado no existe.")
    if int(tour[0]['maxParticipants'] * 0.5) <= data['people']:
      raise ValidationError("La cantidad máxima de personas para una reserva es de: " + str(int(tour[0]['maxParticipants'] * 0.5) - 1))

@reserves.route("/reserves", methods=['POST'])
def post_tours():
  reserve = request.json
  schema = ReservesSchema()
  try:
      result = schema.load(reserve)
  except ValidationError as err:
      return jsonify(err.messages), 400
  # Send data back as JSON
  reserves_collection.insert_reserve(reserve)
  data_now_json_str = json.dumps(result)
  return json.loads(data_now_json_str), 201

@reserves.route("/reserves", methods=['GET'])
def get_reserves():
  if not (request.args.get('tourId') is None):
    return json.loads(reserves_collection.get_reserves_for_tour(request.args.get('tourId'))), 200
  elif not (request.args.get('travelerEmail') is None):
    return json.loads(reserves_collection.get_reserves_for_traveler(request.args.get('travelerEmail'))), 200
  return {"error": "Debe enviar un tourId o travelerEmail para visualizar los tours"}, 400
  