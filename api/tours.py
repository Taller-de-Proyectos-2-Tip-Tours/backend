from flask import Blueprint
from db.tours import ToursCollection
from db.cities import CitiesCollection
from flask import request, jsonify
import json
from marshmallow import Schema, fields, ValidationError, validates_schema

tours = Blueprint('tours',__name__)
tours_collection = ToursCollection()
cities_collection = CitiesCollection()

class ToursSchema(Schema):
    name = fields.String(required=True)
    duration = fields.String(required=True)
    description = fields.String(required=True)
    minParticipants = fields.Integer(required=True)
    maxParticipants = fields.Integer(required=True)
    city = fields.String(required=True)
   
    @validates_schema
    def validate_participants(self, data, **kwargs):
      if data['minParticipants'] > data['maxParticipants']:
        raise ValidationError("The minimum of participants should be less than the maximum")
      
    @validates_schema
    def validate_city(self, data, **kwargs):
      if cities_collection.get_city(data['city']) == None:
        raise ValidationError("The city selected is not available")

@tours.route("/tours", methods=['GET'])
def get_tours():
    return json.loads(tours_collection.get_all_tours()), 200

@tours.route("/tours", methods=['POST'])
def post_tours():
    tour = request.json
    schema = ToursSchema()
    try:
        result = schema.load(tour)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    data_now_json_str = json.dumps(result)

    # Send data back as JSON
    return json.loads(data_now_json_str), 201
    #return tours_collection.insert_one()