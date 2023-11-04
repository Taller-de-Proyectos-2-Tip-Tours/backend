from functools import wraps
from flask import request, jsonify
import firebase_admin
from firebase_admin import auth, credentials
import os

valid_token = "my_secret_token"
cred = credentials.Certificate("config/tip-tours-df5b5-firebase-adminsdk-659l9-e5b2e8dd16.json")
firebase_admin.initialize_app(cred)

def verify_token(id_token):
  try:
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token
  except Exception as e:
    return None

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if os.environ["TESTING"] == "True":
      return f(*args, **kwargs)
    token = request.headers.get('token')
    if not token:
      return jsonify({'error': 'Token inválido'}), 401
    decoded_token = verify_token(token)
    if not decoded_token:
      return jsonify({'error': 'Token inválido'}), 401
    return f(*args, **kwargs)
  return decorated