import requests
import json
from db.users_db import UsersCollection
from db.reserves_db import ReservesCollection

class Notificator:
  _serverToken = "AAAASVPSQX8:APA91bGpxJat6nwLjzgpu9k0k-lf9oFA_65If4VHJWlxVI5RMchWsf_k8GXk4MTvEvl7lrbNHtUVgS_7vZYrCSC0OXdet245twnaVpq-TxPu_ul_GbJYdIgP4kgldg6fT_hplNcyU7FO"
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
