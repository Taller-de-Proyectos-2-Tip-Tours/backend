from flask import Flask
from flask_cors import CORS
from api.tours import tours
from api.cities import cities

app = Flask(__name__)
app.register_blueprint(tours)
app.register_blueprint(cities)

CORS(app)

# main driver function
if __name__ == "__main__":
    app.run(host='0.0.0.0')