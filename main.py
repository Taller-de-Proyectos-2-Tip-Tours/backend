import os
import argparse
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

load_dotenv()
os.environ["TESTING"] = "False"

from flask import Flask
from flask_cors import CORS
from api.tours_api import tours
from api.cities_api import cities
from api.reserves_api import reserves
from api.reviews_api import reviews
from utilities.controller import Controller
from api.admins_api import admins
from api.users_api import users

app = Flask(__name__)
app.register_blueprint(tours)
app.register_blueprint(cities)
app.register_blueprint(reserves)
app.register_blueprint(reviews)
app.register_blueprint(admins)
app.register_blueprint(users)

CORS(app)

parser = argparse.ArgumentParser(description='Reset DB and create example data')

parser.add_argument('--drop_tours', action='store_true', help='set if you want the tour collection to be dropped')
parser.add_argument('--example_tours', action='store_true', help='set if you want example tours to be added')

args = parser.parse_args()

if args.drop_tours:
    print("Droping DB.....")
    from utilities.examples_generator import ToursExampleGenerator
    generator = ToursExampleGenerator()
    try:
        generator.drop_tours()
        generator.drop_reserves()
        generator.drop_reviews()
        generator.drop_users()
    except:
        print("Something went wrong")
    print("Done")

if args.example_tours:
    print("Generating examples.....")
    from utilities.examples_generator import ToursExampleGenerator
    generator = ToursExampleGenerator()
    try:
        generator.generate_examples()
    except:
        print("Something went wrong")
    print("Done")

controller = Controller()

# main driver function
if __name__ == "__main__" and (not args.example_tours) and (not args.drop_tours):
    scheduler = BackgroundScheduler()
    scheduler.add_job(controller.end_tours, 'interval', minutes=60)
    scheduler.add_job(controller.reserve_reminder, 'interval', minutes=60)
    scheduler.start()
    app.run(host='0.0.0.0')
    scheduler.shutdown()
