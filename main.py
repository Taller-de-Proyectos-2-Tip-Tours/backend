import os
import argparse

os.environ["TESTING"] = "False"

from flask import Flask
from flask_cors import CORS
from api.tours_api import tours
from api.cities_api import cities
from api.reserves_api import reserves
from api.reviews_api import reviews

app = Flask(__name__)
app.register_blueprint(tours)
app.register_blueprint(cities)
app.register_blueprint(reserves)
app.register_blueprint(reviews)

CORS(app)

parser = argparse.ArgumentParser(description='Reset DB and create example data')

parser.add_argument('--drop_tours', action='store_true', help='set if you want the tour collection to be dropped')
parser.add_argument('--example_tours', action='store_true', help='set if you want example tours to be added')

args = parser.parse_args()

if args.drop_tours:
    print("Droping DB.....")
    from tests.examples_generator import ToursExampleGenerator
    generator = ToursExampleGenerator()
    try:
        generator.drop_tours()
        generator.drop_reserves()
    except:
        print("Something went wrong")
    print("Done")

if args.example_tours:
    print("Generating examples.....")
    from tests.examples_generator import ToursExampleGenerator
    generator = ToursExampleGenerator()
    try:
        generator.generate_examples()
    except:
        print("Something went wrong")
    print("Done")

# main driver function
if __name__ == "__main__" and (not args.example_tours) and (not args.drop_tours):
   app.run(host='0.0.0.0')