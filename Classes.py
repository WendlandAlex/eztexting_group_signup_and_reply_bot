from email import message
import requests
from logging import Logger

from sympy import comp

class Client():
    def __init__(self, username, password, companyName, base_url, payload={}, headers={}):
        self.payload = payload
        self.headers = headers
        self.username = username
        self.password = password
        self.companyName = companyName
        self.base_url = base_url
        self.oauth_token = self.generate_oauth_token(self.username, self.password)
        self._update_payload(self, companyName)
        self._update_headers(self, self.oauth_token)
        
    def generate_oauth_token(username, password):
        # TODO:
        return "auth"

    def _update_payload(self, **kwargs):
        self.payload.update(kwargs)

    def _update_headers(self, **kwargs):
        self.headers.update({
                "Accept": "*/*",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.oauth_token}"
                })
        self.headers.update(kwargs)

    def make_api_call(self, method, url, headers_dict=None, payload_dict=None):
        try:
            final_headers = self.headers.update(headers_dict)
            final_payload = self.payload.update(payload_dict)

            response =  requests.request(
                    verb=method,
                    url=url,
                    headers=final_headers,
                    payload=final_payload
                )

            if not response.ok:
                Logger.error(f'ERROR {response.status_code} CALLING {response.url}: {response.json()}')
            else:
                return {
                    'status_code': response.status_code,
                    'data': response.json()
                }
        
        except Exception as e:
            Logger.error(f'ERROR CALLING {url}: {e}')


class Contact(Client):
    def __init__(self, contact_id=None):
        self.contact_id = contact_id
        self.url=f'{self.base_url}/contacts'
        data = self._get_contact()
        if data is not None:
            for field, value in data.items():
                setattr(self, field, value)

    def _get_contact(self):
        return super().make_api_call(
            url = f'{self.url}/{self.contact_id}',
            method = 'GET'
        ).get('data').get('Response').get('Entry')

    def create(self, query_params_dict):
        return super().make_api_call(
            url = self.url,
            method = 'GET',
            params_dict=query_params_dict
        ).get('data').get('Response').get('Entry')

    def update(self, query_params_dict):
        """
        The only intended use case for this method is to immediately precede deleting the class instance
        So expect that any service calling this method will accept the return object and call 'del old_object'
        """
        response = super().make_api_call(
            url = f'{self.url}/{self.contact_id}',
            method = 'GET',
            params_dict=query_params_dict
        ).get('data').get('Response').get('Entry')

        return Contact(response.get('ID'))

    def delete(self):
        response = super().make_api_call(
            url = f'{self.url}/{self.contact_id}',
            method = 'DELETE'
        )

        if response.get('status_code') == 204:
            return self.contact_id


class CreditCard(Client):
    def __init__(self, last_four_digits):
        self.url=f'{self.base_url}/billing/credits'
        if last_four_digits is not None: self.last_four_digits = last_four_digits
        credits_data = self._get_available_credits()
        self.TotalCredits = credits_data.get('TotalCredits')
        self.PlanCredits = credits_data.get('PlanCredits')
        self.AnytimeCredits = credits_data.get('AnytimeCredits')
        
    def _get_available_credits(self):
        response = super().make_api_call(
            url = f'{self.url}/get',
            method = 'GET'
        )
        
        try:
            credits = response.get('data').get('Response').get('Entry')
        except KeyError:
            credits = None

        return credits

class Folder():
    pass


class Group():
    pass


class Inbox():
    pass


class Keyword():
    pass


class MediaFile():
    pass


class Message(Client):
    def __init__(self, companyName=None, fromNumber=None, groupIds=[]):
        self.url                = f'{self.base_url}/messages'
        self.companyName        = companyName
        self.fromNumber         = fromNumber
        self.groupIds           = groupIds
        self.mediaFielId        = mediaFileId
        self.mediaurl           = mediaUrl
        self.Message            = message
        self.messageTemplateId  = messageTemplateId
        self.strictValidation   = strictValidation
        self.toNumbers          = toNumbers

    def _load_params(self):
        # transform instance attributes into a dict to pass to the requests method
        # but remove url and treat url as its own parameter
        params_dict = self.__dict__
        params_dict.pop('url')
        return params_dict

    def send(self):
        response = super().make_api_call(
            url = self.url,
            method = 'GET', # did they really have to put a write operation behind a GET?
            params_dict = self._load_params()
        )

        if response.get('status_code') == 201:
            return response.get('data').get('Reponse').get('Entry')