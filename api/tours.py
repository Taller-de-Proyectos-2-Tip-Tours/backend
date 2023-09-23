from db.tours import ToursCollection
from db.cities import CitiesCollection
from flask import request, jsonify, Blueprint
import json
from marshmallow import Schema, fields, ValidationError, validates_schema
import time
from datetime import datetime

tours = Blueprint('tours',__name__)
tours_collection = ToursCollection()
cities_collection = CitiesCollection()

lenguages = ["Español", "Inglés", "Portugués", "Alemán", "Francés", "Italiano"]

class ToursSchema(Schema):
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
    lat = fields.String(required=True)
    lon = fields.String(required=True)

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
       if length < 2 or length > 4:
          raise ValidationError("El paseo debe contener entre 2 y 4 imagenes extras")

@tours.route("/tours", methods=['GET'])
def get_tours():
    return json.loads(tours_collection.get_all_tours(request.args.get('name'), request.args.get('city'))), 200

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
    tours_collection.insert_tour(tour)
    data_now_json_str = json.dumps(result)
    return json.loads(data_now_json_str), 201