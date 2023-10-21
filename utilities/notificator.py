import requests
import json

class Notificator:
  _serverToken = "hola"
  _deviceToken = "chau"

  def send_notification(self, title, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + self._serverToken,
      }
    body = {'notification': { 'title': title, 'body': message },
              'to': self._deviceToken,
              'priority': 'high'
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)
    print(response.json())
