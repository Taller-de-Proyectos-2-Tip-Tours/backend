import datetime
from flask import request, Blueprint
import json
from db.admins_db import AdminsCollection
from utilities.authentication import app_token
import jwt
import os

admins = Blueprint('admins',__name__)
admins_collection = AdminsCollection()

def generate_token(username):
  payload = {
    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2),
    'iat': datetime.datetime.utcnow(),
    'sub': username
  }
  return jwt.encode(
    payload,
    os.getenv("encryptKey"),
    algorithm='HS256'
  )

@admins.route("/admins/login", methods=['POST'])
@app_token(expected_tokens=[os.getenv("backofficeToken")])
def admins_login():
  credentials = request.json
  admin = json.loads(admins_collection.get_admin(credentials.get("username"), credentials.get("password")))
  if admin is None:
    return {"error": "Usuario o contraseña incorrecto"}, 400    
  token = generate_token(credentials.get("username"))
  return {"success": "Login exitoso", "token": token}, 200