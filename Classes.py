import base64
import datetime
import requests
from logging import Logger

from Services.oauth import generate_oauth_token, refresh_oauth_token


class Client():
    def __init__(self, username, password, companyName, base_url, payload={}, headers={}):
        self.payload = payload
        self.headers = headers
        self.headers.update({"Accept": "*/*", "Content-Type": "application/json"})
        self.username = username
        self.password = password
        self.companyName = companyName
        self.base_url = base_url
        self._generate_or_refresh_oauth_token(self.username, self.password)
        self._update_payload(self, companyName)
        self._update_headers(self, self.accessToken)

    def _update_payload(self, **kwargs):
        self.payload.update(kwargs)

    def _update_headers(self, **kwargs):
        self.headers.update(kwargs)

    def _generate_or_refresh_oauth_token(self):
        if all(hasattr(self, attribute) for attribute in ['accessToken', 'refreshToken', 'expiration_datetime']):
            # refresh the token if it expires in the next 10 seconds
            if self.expiration_datetime < datetime.datetime.now() + datetime.timedelta(seconds=10):
                accessToken, refreshToken, expiration_datetime = refresh_oauth_token(self, self.refreshToken)

                self.accessToken = accessToken
                self.refreshToken = refreshToken
                self.expiration_datetime = expiration_datetime

        else:
            accessToken, refreshToken, expiration_datetime = generate_oauth_token(self.username, self.password)

            self.accessToken = accessToken
            self.refreshToken = refreshToken
            self.expiration_datetime = expiration_datetime

    def make_api_call(self, method, url, headers_dict=None, payload_dict=None, auth_method='oauth'):
        if auth_method == 'oauth':
            auth_header = {f'Authorization: Bearer {self.accessToken}'}

        elif auth_method == 'http_basic':
            auth_string = ':'.join([self.username, self.password])
            b64_encoded_auth_string = base64.b64encode(auth_string.encode())
            auth_header = {f'Authorization: Basic {b64_encoded_auth_string}'}

        try:
            final_headers = self.headers.update(headers_dict).update(auth_header)
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
    def __init__(self, fromNumber: str=None, groupIds: list=None, mediaFileId: str=None, mediaUrl: str=None, message: str=None, messageTemplateId: str=None, sendAt: str=None, strictValidation: bool=False, toNumbers: list=None, headers: dict=None):
        """
        strictValidation = if one number in the list is invalid, no messages will be sent (including to valid numbers)
        """
        # params from eztexting documentation
        self.companyName        = self.companyName
        self.fromNumber         = fromNumber
        self.groupIds           = groupIds
        self.mediaFileId        = mediaFileId
        self.mediaUrl           = mediaUrl
        self.message            = message
        self.messageTemplateId  = messageTemplateId
        self.sendAt             = sendAt
        self.strictValidation   = strictValidation
        self.toNumbers          = toNumbers

        # params we need to make the API call
        self.url                = f'{self.base_url}/messages'
        self.headers            = headers


    def _load_payload(self):
        # transform instance attributes into a dict to pass to the requests method
        # but remove url and treat url as its own parameter
        payload_dict = self.__dict__
        payload_dict.pop('url')
        return payload_dict

    def send(self):
        response = super().make_api_call(
            url = self.url,
            method = 'POST',
            headers_dict = self.headers,
            payload_dict = self._load_payload()
        )

        if response.get('status_code') in [200, 201]:
            return response.get('data').get('id')