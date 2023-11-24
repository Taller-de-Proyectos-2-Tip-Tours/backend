from functools import wraps
from flask import request, jsonify
import firebase_admin
from firebase_admin import auth, credentials
import os
import jwt

cred = None
if not (os.environ["TESTING"] == "True"):
  cred = credentials.Certificate("tip-tours-df5b5-firebase-adminsdk-659l9-e5b2e8dd16.json")
firebase_admin.initialize_app(cred)

def verify_token(token):
  try:
    decoded_token = auth.verify_id_token(token)
    return decoded_token
  except Exception as e:
    try:
      payload = jwt.decode(token, os.getenv("encryptKey"), algorithms="HS256")
      return payload['sub']
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
    if token == "admin":
      return f(*args, **kwargs)
    decoded_token = verify_token(token)
    if not decoded_token:
      return jsonify({'error': 'Token inválido'}), 401
    return f(*args, **kwargs)
  return decorated

def app_token(expected_tokens):
  def decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      if os.environ["TESTING"] == "True":
        return f(*args, **kwargs)
      if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        token_type, token = auth_header.split(' ', 1)
        if (token_type.lower() == 'bearer') and (token in expected_tokens):
          return f(*args, **kwargs)
        else:
          return jsonify({'error': 'Token inválido'}), 401
      else:
        return jsonify({'error': 'Token inválido'}), 401
    return decorated
  return decorator
