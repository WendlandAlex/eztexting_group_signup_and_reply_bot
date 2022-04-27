import requests
from logging import Logger

from sympy import re

class Client():
    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.base_params_dict = {
            "User": self.username,
            "Password": self.password,
            "format": "json"
        }

    def make_api_call(self, url, method, params_dict=None):
        if method.lower() not in ['get', 'post']:
            Logger.error(f'ERROR: invalid HTTP method provided {method}')
            raise

        new_params_dict = self.base_params_dict.update(params_dict)

        response =  requests.request(
                verb=method,
                url=url,
                params=new_params_dict
            )

        if not response.ok:
            Logger.error(f'ERROR {response.status_code} CALLING {response.url}: {response.json()}')
        
        else:
            return response.json().get('Response')

class Contact():
    pass

class CreditCard(Client):
    def __init__(self, last_four_digits):
        self.url=f'{self.base_url}/billing/credits'
        self.last_four_digits = last_four_digits
        credits_breakdown_dict = self._get_available_credits()
        self.available_credits = credits_breakdown_dict.get('TotalCredits')
        self.available_credits_plan = credits_breakdown_dict.get('PlanCredits')
        self.available_credits_anytime = credits_breakdown_dict.get('AnytimeCredits')
        
    def _get_available_credits(self):
        response = super(CreditCard).make_api_call(
            url = f'{self.url}/get',
            method = 'GET',
        )

        return response.get('Entry')

class Folder():
    pass

class Group():
    pass

class Inbox():
    pass

class Keyword():
    pass

class Message():
    pass