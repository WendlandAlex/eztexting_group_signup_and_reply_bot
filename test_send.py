from __future__ import annotations
from typing import TYPE_CHECKING
TYPE_CHECKING = True

if TYPE_CHECKING:
    from Handlers.validators import create_hmacSHA1_hash

import os
import dotenv
import requests
import time
import base64
import random


dotenv.load_dotenv()
url_data = os.getenv('WEBHOOK_URL')
signing_key = os.getenv('WEBHOOK_SECRET_KEY')

days_list = [
        'Monday by the way I have a long message... (1/99)',
        'tuesday',
        'teusday',
        'Wednesday and Friday!',
        'monday\, tuesday\, wednesday\, thursday\, and friday',
        " ",
        "unsubscribe",
        "Thursday 🤠", 
        f'Saturday {"🤠".encode()}'
    ]

def generate_body(inputs_list):
    i = random.randint(0,len(inputs_list)-1)

    # documentation for schema:
    # https://developers.eztexting.com/docs/webhooks-1#json-webhook-postback-example-for-an-inbound-text-received
    return {
    "id":"123",
    "type": "inbound_text.received",
    "fromNumber":"14243798239",
    "toNumber":"14243798231",
    "message":f"I want to sign up for {inputs_list[i]}",
    "received":"2020-03-06T10:31:18.724Z",
    "optIn": False,
    "optOut": False
    }

def generate_header_sig(body):
    return {
        "X-Signature": base64.b64encode(create_hmacSHA1_hash(body, signing_key=signing_key).digest()).decode()
        }

def main(url, data):
    response = requests.post(
        url=url+'/inbound_sms_received',
        headers=generate_header_sig(data),
        json=data
    )

    # print(response.headers, response.json())
    print(response.status_code, response.json().get('message'))

if __name__ == '__main__':
    while True:
        main(url_data, generate_body(days_list))
        time.sleep(0.75)