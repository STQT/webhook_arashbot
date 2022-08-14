import random

from base64 import b64encode
import requests
from configs import SMS_SECRET_KEY

URL = 'http://91.204.239.44/broker-api/send'
credentials = SMS_SECRET_KEY
encodedCredentials = str(b64encode(credentials.encode("utf-8")), "utf-8")
AUTHORIZATION = {
    "Authorization": f"Basic {encodedCredentials}",
    "Content-Type": "application/json"
}


def sent_sms(user_sms, phone_number):
    sms_id = random.randint(0, 5000)
    data = {
        "messages": [
            {
                "recipient": f"{phone_number}",
                "message-id": f"abc{sms_id}",
                "sms": {
                    "originator": "3700",
                    "message-id": f"abc{sms_id}",
                    "content": {
                        "text": user_sms
                    }
                }
            }
        ]

    }
    response = requests.post(url=URL, json=data, headers=AUTHORIZATION)
    result = response.status_code
    if result == 200:
        return True
