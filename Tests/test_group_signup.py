from utils import send_sms, create_hmacSHA1_hash

import os
import dotenv
dotenv.load_dotenv()
url_data = os.getenv('WEBHOOK_SERVER_URL', None)
signing_key = os.getenv('WEBHOOK_SERVER_SECRET_KEY')
LOCAL_ONLY = os.getenv('LOCAL_ONLY', None)
if LOCAL_ONLY == True:
    url_data = 'http://localhost:8080'

base_data = {
    "id":"123",
    "type": "inbound_text.received",
    "fromNumber":"14243798239",
    "toNumber":"14243798231",
    "message": None,
    "received":"2020-03-06T10:31:18.724Z",
    "optIn": False,
    "optOut": False
    }


def test_signup_single_valid():
    test_data = base_data.copy()
    test_data['message'] = 'yeehaw sign me up for Thursday, partner 🤠'
    response = send_sms(url_data, test_data, signing_key)
    assert response.ok and response.json().get('message').lower().find('thursday')

def test_signup_multiple_valid():
    test_data = base_data.copy()
    test_data['message'] = 'Wednesday and Friday!'
    response = send_sms(url_data, test_data, signing_key)
    assert response.ok and response.json().get('message').lower().find('wednesday, friday')


def test_signup_invalid():
    test_data = base_data.copy()
    test_data['message'] = 'there are no weekday names in this message'
    response = send_sms(url_data, test_data, signing_key)
    assert not response.ok