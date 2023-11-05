from flask import request, jsonify, Blueprint
import json
from db.admins_db import AdminsCollection
from utilities.authentication import token_required

admins = Blueprint('admins',__name__)
admins_collection = AdminsCollection()

@admins.route("/admins/login", methods=['POST'])
def admins_login():
  credentials = request.json
  admin = json.loads(admins_collection.get_admin(credentials.get("username"), credentials.get("password")))
  if admin is None:
    return {"error": "Usuario o contraseña incorrecto"}, 400    
  return {"success": "Login exitoso"}, 200