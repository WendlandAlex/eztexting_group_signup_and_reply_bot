from __future__ import annotations
from typing import TYPE_CHECKING

TYPE_CHECKING = True
if TYPE_CHECKING:
    from webhook_server.Handlers.validators import create_hmacSHA1_hash

import os
import requests
import base64

def generate_header_sig(body=None, signing_key=None):
    a = {
        "X-Signature": base64.b64encode(create_hmacSHA1_hash(body, signing_key).digest()).decode()
        }

    return a

def send_sms(url, data, signing_key):
    return requests.request(
        method='POST',
        url=url+'/inbound_text_received',
        headers=generate_header_sig(data, signing_key),
        json=data
    )
