from flask import Flask
from db import Database

app = Flask(__name__)
db = Database()

@app.route("/tours")
def get_tours():
    return db.get_all_tours()

# main driver function
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--dropdb', help='send if you want the db to be droped', action='store_true')
    args = parser.parse_args()
    if args.dropdb != None:
        db.drop_tours_collection()
        db.create_tours_collection(True)
    app.run(host='0.0.0.0')