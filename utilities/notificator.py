import requests
import json
from db.users_db import UsersCollection
from db.reserves_db import ReservesCollection
import os

class Notificator:
  _serverToken = os.getenv("serverToken")
  _reserves = ReservesCollection()
  _users = UsersCollection()

  def _send_notification(self, title, message, deviceToken, data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + self._serverToken,
      }
    body = {'notification': { 'title': title, 'body': message }, 
            'data': data,
              'to': deviceToken,
              'priority': 'high'
            }
    print(body)
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)
    print(response.json())

  def notify_cancelled_tour_date(self, userEmail, tourData):
    tokens = self._users.get_device_token_by_email(userEmail)
    for token in tokens:
      self._send_notification("Paseo cancelado", 
                              "Disculpe, la fecha de su paseo ha sido cancelado. Lamentamos cualquier inconveniente causado.", 
                              token,
                              tourData)

  def notify_modified_tour(self, userEmail, tourData):
    tokens = self._users.get_device_token_by_email(userEmail)
    for token in tokens:
      self._send_notification("Paseo modificado", 
                              "Se ha realizado un cambio en los detalles de su paseo. Le solicitamos revisar la información actualizada.", 
                              token,
                              tourData)
      
  def notify_reserve_reminder(self, userEmail, tourData):
    tokens = self._users.get_device_token_by_email(userEmail)
    for token in tokens:
      self._send_notification("Recordatorio de reserva", 
                              "Recuerde que tiene una reserva para un paseo a menos de 24 horas. Le solicitamos revisar los detalles y prepararse.", 
                              token,
                              tourData)
