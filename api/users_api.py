from flask import request, Blueprint
import json
from db.users_db import UsersCollection

users = Blueprint('users',__name__)
users_collection = UsersCollection()

def register_user(userEmail, token):
    token = []
    token.append(token)
    user_db = {
        "userEmail": userEmail,
        "devicesTokens": token
    }
    users_collection.create_new_user(user_db)
    return {"success": "Usuario registrado correctamente"}, 200

@users.route("/users/login", methods=['POST'])
def login_user():
    user = request.json
    if not (user["userEmail"] and user["deviceToken"]):
      return {"error": "El usuario debe tener un email y dispositivo"}, 400
    existing_user = users_collection.get_user_by_email(user["userEmail"])
    if existing_user is None:
      token = []
      token.append(user["deviceToken"])
      user_db = {
          "userEmail": user["userEmail"],
          "devicesTokens": token
      }
      users_collection.create_new_user(user_db)
      return {"success": "Usuario registrado correctamente"}, 200
    elif not (user["deviceToken"] in existing_user["devicesTokens"]):
      users_collection.add_new_token(user["userEmail"], user["deviceToken"])
    return {"success": "El usuario inició sesión correctamente"}, 200

