import requests
import json

class Notificator:
  _serverToken = "AAAASVPSQX8:APA91bGxjsKTkHWF5FEEg7ZCvCORC3F_oYFBw4kvOJ2EInaYKYnuhXtqFVyEk9f1_YJvZgo-QJ_Bwf1i5gK_d88bNzxGJZK1ED-g5vaomCzfPjm0fblPyE2W0l6VI1K45OOH1crYlA1A"
  _deviceToken = "caiM-UoJTcOAohL64R3qMu:APA91bFDyX8UDCQXts12xWPTDYLCRT5CEpTrk18P5zHpELORahg34IYhj_e3J27lEoNozUAMJyGn_0BT_sGN0EuqOZ0gQ3ZC2s6kGdG0KWR4f6KxHHpt-xEjVXlo0Jm67UggNO1j4aKX"

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
