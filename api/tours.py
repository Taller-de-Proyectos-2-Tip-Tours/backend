from flask import Blueprint
from db.tours import ToursCollection
from flask import request, jsonify
from json import dumps
from marshmallow import Schema, fields, ValidationError, validates_schema

tours = Blueprint('tours',__name__)
tours_collection = ToursCollection()

class ToursSchema(Schema):
    name = fields.String(required=True)
    duration = fields.String(required=True)
    description = fields.String(required=True)
    minParticipants = fields.Integer(required=True)
    maxParticipants = fields.Integer(required=True)

    @validates_schema
    def validate_participants(self, data, **kwargs):
      if data['minParticipants'] > data['maxParticipants']:
        raise ValidationError("The minimum of participants should be less than the maximum")

@tours.route("/tours", methods=['GET'])
def get_tours():
    return tours_collection.get_all_tours()

@tours.route("/tours", methods=['POST'])
def post_tours():
    tour = request.json
    schema = ToursSchema()
    try:
        result = schema.load(tour)
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400
    data_now_json_str = dumps(result)

    # Send data back as JSON
    return jsonify(data_now_json_str), 200
    #return tours_collection.insert_one()