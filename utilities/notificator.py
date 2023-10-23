import requests
import json
from db.users_db import UsersCollection

class Notificator:
  _serverToken = "hola"
  _deviceToken = "chau"
  _users = UsersCollection()

  def _send_notification(self, title, message, deviceToken):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + self._serverToken,
      }
    body = {'notification': { 'title': title, 'body': message },
              'to': deviceToken,
              'priority': 'high'
            }
    print(body)
    #response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    #print(response.status_code)
    #print(response.json())

  def notify_cancelled_tour_date(self, userEmail):
    tokens = self._users.get_device_token_by_email(userEmail)
    for token in tokens:
      self._send_notification("Paseo cancelado", 
                              "Disculpe, la fecha de su paseo ha sido cancelado. Lamentamos cualquier inconveniente causado.", 
                              token)
