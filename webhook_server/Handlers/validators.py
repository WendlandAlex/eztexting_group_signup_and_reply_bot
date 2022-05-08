import base64
import json
import hashlib
import hmac
import os
from dotenv import load_dotenv

# Webhook documentation
# https://developers.eztexting.com/docs/webhooks-1
"""EZ Texting webhooks can optionally include a secret token that, \
    if included, is used as a secret key to create a HmacSHA1 hash of \
    the JSON payload, returned in an 'X-Signature' header. \
    This header can then be used to verify the callback POST \
    is coming from EZ Texting.
"""

def validate_hash_from_header(header, body, signing_key: str):
    hashed_body_bytes = create_hmacSHA1_hash(body, signing_key) # returns a hashlib object

    # compare this hash to hash sent by the remote host in the
    # 'X-Signature' header to prove they have the shared secret
    hashed_body_string = base64.b64encode(hashed_body_bytes.digest()).decode()
    
    if header == hashed_body_string:
        return True

    return False

def create_hmacSHA1_hash(input, signing_key):
    if signing_key:
        if type(signing_key) is bytes:
            bytes_key = signing_key
        elif type(signing_key) is str:
            bytes_key = signing_key.encode('utf-8')
    else:
        raise
    
    if input:
        if type(input) is dict:
            bytes_body = json.dumps(input).encode('utf-8')
        elif type(input) is str:
            bytes_body = input.encode('utf-8')
        elif type(input) is bytes:
            bytes_body = input
        else:
            raise TypeError
    else:
        raise

    return hmac.new(key=bytes_key, msg=bytes_body, digestmod=hashlib.sha1)
    