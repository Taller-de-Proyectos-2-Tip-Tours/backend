from flask import request, jsonify, Blueprint
import json
from marshmallow import Schema, fields, ValidationError, validates_schema
from db.tours_db import ToursCollection
from bson.objectid import ObjectId
from db.reserves_db import ReservesCollection
from datetime import datetime, timedelta
import pytz
from utilities.authentication import token_required, app_token
import os

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
    tour = json.loads(tours_collection.get_tour_by_id(data['tourId'], {'maxParticipants': 1}))
    if tour is None:
      raise ValidationError("El tour seleccionado no existe.")
    reserves = json.loads(reserves_collection.get_reserves_for_traveler_tour(data["traveler"]["email"], data['tourId']))
    people = sum(reserve["people"] for reserve in reserves)
    if int(tour['maxParticipants'] * 0.5) < (data['people'] + people):
      raise ValidationError("La cantidad máxima de personas para una reserva es de: " + str(int(tour['maxParticipants'] * 0.5)))

@reserves.route("/reserves", methods=['POST'])
@app_token(expected_tokens=[os.getenv("mobileAppToken")])
@token_required
def post_reserve():
  reserve = request.json
  schema = ReservesSchema()
  try:
      result = schema.load(reserve)
  except ValidationError as err:
      return jsonify(err.messages), 400
  tour = json.loads(tours_collection.get_tour_by_id(reserve['tourId'], {'maxParticipants': 1, 'dates': 1}))
  new_dates = []
  reserve_created = False
  for date in tour["dates"]:
    if date["date"] == result["date"] and date["state"] == "abierto":
      argentina_timezone = pytz.timezone('America/Argentina/Buenos_Aires')
      tour_date = argentina_timezone.localize(datetime.strptime(date["date"], "%Y-%m-%dT%H:%M:%S"))
      time_difference = tour_date - datetime.now(argentina_timezone)
      if time_difference < timedelta(hours=24):
          return {
            "error": "No puede crear una reserva a menos de 24 horas de la misma." 
          }, 400
      if date["people"] + result["people"] > tour["maxParticipants"]:
        return {"error": "La cantidad de personas de la reserva supera la capacidad del tour"}, 400
      else:
        reserve_created = True
        date["people"] += result["people"]
      if date["people"] == tour["maxParticipants"]:
        date["state"] = "cerrado"
    new_dates.append(date)
  if reserve_created == False:
    return {"error": "La fecha seleccionada no se encuentra disponible."}, 400
  reserve["state"] = "abierto"
  reserve = json.loads(reserves_collection.insert_reserve(reserve))
  tours_collection.update_tour_dates(new_dates, result["tourId"])
  return {'success': 'La reserva fue creada con éxito.', 'id': reserve['$oid']}, 201

@reserves.route("/reserves", methods=['GET'])
@app_token(expected_tokens=[os.getenv("backofficeToken"), os.getenv("webAppToken"), os.getenv("mobileAppToken")])
@token_required
def get_reserves():
  reserves_list = {}
  if (request.args.get('tourId') is None) and (request.args.get('travelerEmail') is None):
    return {"error": "Debe enviar un tourId o travelerEmail para visualizar los tours"}, 400
  if not (request.args.get('tourId') is None):
    reserves_list = json.loads(reserves_collection.get_reserves_for_tour(request.args.get('tourId')))
  else:
    reserves_list = json.loads(reserves_collection.get_reserves_for_traveler(request.args.get('travelerEmail')))
  for reserve in reserves_list:
    tour = json.loads(tours_collection.get_tour_by_id(reserve['tourId'], {'name': 1, 'dates': 1}))
    reserve['tourName'] = tour['name']
  return reserves_list, 200

@reserves.route("/reserves/<reserveId>", methods=['DELETE'])
@token_required
@app_token(expected_tokens=[os.getenv("mobileAppToken")])
def cancel_reserve(reserveId):
  try:
    reserve = json.loads(reserves_collection.get_reserve_by_id(reserveId))
    if reserve is None:
      return {
          "error": "La reserva no existe." 
        }, 400
    time_difference = datetime.strptime(reserve["date"], "%Y-%m-%dT%H:%M:%S") - datetime.now()
    if time_difference < timedelta(hours=24):
        return {
          "error": "No puede cancelar una reserva a menos de 24 horas de la misma." 
        }, 400
    reserves_collection.change_reserve_state(reserveId, "cancelado")
    tours_collection.cancel_reserve_for_tour(reserve["tourId"], reserve["date"], reserve["people"])
  except Exception as err:
    return {"error": str(err)}, 404
  return {"success": "La reserva fue cancelada correctamente"}, 200
  