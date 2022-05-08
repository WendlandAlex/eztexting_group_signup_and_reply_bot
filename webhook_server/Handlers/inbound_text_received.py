from __future__ import annotations
from typing import TYPE_CHECKING
TYPE_CHECKING = True
if TYPE_CHECKING:
    from Classes.Subclass import Contact

import flask
import re
import redis
import rq
import requests
import os
import json

from task_queue import out_queue

def send_confirmation(contact: "Contact", groupNames: list, queue=False):
    capitalized_groups = [i.capitalize() for i in groupNames]
    if len(capitalized_groups) > 1:
        capitalized_groups_string = ', '.join(capitalized_groups[:-2] + [' and '.join(capitalized_groups[-2:])])
    else:
        capitalized_groups_string = capitalized_groups[0]

    json_data = {'toNumbers': [contact.phoneNumber], 'message': f'Thank you for signing up for {capitalized_groups_string}!'}
    
    response = requests.Request(
        method='POST',
        url='https://eztexting_api_endpoint.com',
        headers={'X-Authorization': 'Bearer oauthgoeshere'},
        json=json_data
    )

    response = response.prepare()

    return flask.Response(json.dumps({'message': json_data.get("message")}), 200, mimetype="application/json")
