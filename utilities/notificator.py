import requests
import json
from db.users_db import UsersCollection
from db.reserves_db import ReservesCollection
import os

class Notificator:
  _serverToken = os.getenv("serverToken")
  _reserves = ReservesCollection()
  _users = UsersCollection()

  def _send_notification(self, title, message, deviceToken, data, image = os.getenv("neutralImage")):
    print(image)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + self._serverToken,
      }
    body = {'notification': { 'title': title, 'body': message, 'image': image }, 
            'data': data,
              'to': deviceToken,
              'priority': 'high'
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.json())
    if response.json()['failure']:
      raise Exception("Unable to notify User") 
    print(response.status_code)

  def notify_cancelled_tour_date(self, userEmail, tourData):
    tokens = self._users.get_device_token_by_email(userEmail)
    updatedDeviceTokens = []
    for token in tokens["devicesTokens"]:
      try:
        self._send_notification("Paseo cancelado", 
                                "Disculpe, la fecha de su paseo ha sido cancelado. Lamentamos cualquier inconveniente causado.", 
                                token,
                                tourData,
                                os.getenv("sadImage"))
        updatedDeviceTokens.append(token)
      except Exception as e:
        print(e)
    self._users.update_device_tokens_for_user(tokens["_id"]["$oid"], updatedDeviceTokens)

  def notify_modified_tour(self, userEmail, tourData):
    tokens = self._users.get_device_token_by_email(userEmail)
    updatedDeviceTokens = []
    print(userEmail)
    for token in tokens["devicesTokens"]:
      try:
        self._send_notification("Paseo modificado", 
                                "Se ha realizado un cambio en los detalles de su paseo. Le solicitamos revisar la información actualizada.", 
                                token,
                                tourData)
        updatedDeviceTokens.append(token)
      except Exception as e:
        print(e)
    self._users.update_device_tokens_for_user(tokens["_id"]["$oid"], updatedDeviceTokens)

  def notify_reserve_reminder(self, userEmail, tourData):
    tokens = self._users.get_device_token_by_email(userEmail)
    updatedDeviceTokens = []
    for token in tokens["devicesTokens"]:
      try:
        self._send_notification("Recordatorio de reserva", 
                                "Recuerde que tiene una reserva para un paseo a menos de 24 horas. Le solicitamos revisar los detalles y prepararse.", 
                                token,
                                tourData,
                                os.getenv("happyImage"))
        updatedDeviceTokens.append(token)
      except Exception as e:
        print(e)
    self._users.update_device_tokens_for_user(tokens["_id"]["$oid"], updatedDeviceTokens)
    if len(updatedDeviceTokens) == 0:
      raise Exception("No device token available for user")
