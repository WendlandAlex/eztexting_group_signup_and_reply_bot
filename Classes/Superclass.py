import base64
import datetime
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
classes_logger = logging.getLogger(__name__)
classes_logger.setLevel(logging.DEBUG)

from Services.oauth import generate_oauth_token, refresh_oauth_token


class Client():
    def __init__(self, username=None, password=None, companyName=None, base_url=None, payload={}, headers={}):
        self.payload = payload
        self.headers = headers
        self.username = username
        self.password = password
        self.companyName = companyName
        self.base_url = base_url
        self._generate_or_refresh_oauth_token()
        self._update_payload(**{"companyName": self.companyName})
        self._update_headers(**{"Accept": "*/*", "Content-Type": "application/json"})

        # identify the core set of attributes needed for all API calls
        # subclasses of API class can inherit these by overriding __getattr__ to call the superclass's attributes
        self._attrs_for_subclass = ['companyName', 'base_url', 'headers', 'payload', 'accessToken', 'refreshToken']

    def __str__(self):
        return self.__dict__

    def _update_payload(self, **kwargs):
        if self.payload is None:
            self.payload = kwargs
        else:
            self.payload.update(kwargs)

        return self

    def _update_headers(self, **kwargs):
        if self.headers is None:
            self.headers = kwargs
        else:
            self.headers.update(kwargs)

        return self

    def _generate_or_refresh_oauth_token(self):
        if all(hasattr(self, attribute) for attribute in ['accessToken', 'refreshToken', 'expiration_datetime']):
            # refresh the token if it expires in the next 10 seconds
            if self.expiration_datetime < datetime.datetime.now() + datetime.timedelta(seconds=10):
                accessToken, refreshToken, expiration_datetime = refresh_oauth_token(self, self.refreshToken)

                self.accessToken = accessToken
                self.refreshToken = refreshToken
                self.expiration_datetime = expiration_datetime

        else:
            accessToken, refreshToken, expiration_datetime = generate_oauth_token(self, self.username, self.password)

            self.accessToken = accessToken
            self.refreshToken = refreshToken
            self.expiration_datetime = expiration_datetime

        return self

    def make_api_call(self, method, url, headers_dict: dict=None, payload_dict: dict=None, params_dict: dict=None, auth_method='oauth'):
        final_headers = {}
        final_payload = {}
        final_params  = {}

        if auth_method == 'oauth':
            auth_header = {'Authorization': f'Bearer {self.accessToken}'}

        elif auth_method == 'http_basic':
            auth_string = ':'.join([self.username, self.password])
            b64_encoded_auth_string = base64.b64encode(auth_string.encode())
            auth_header = {'Authorization': f'Basic {b64_encoded_auth_string.decode()}'}

        try:
            for i in [self.headers, headers_dict, auth_header]:
                final_headers.update(i)

            for i in [self.payload, payload_dict]:
                final_payload.update(i)

            if params_dict is not None:
                final_params.update(params_dict) # reserved for future modifications if we need them

            response =  requests.request(
                    method=method,
                    url=url,
                    headers=final_headers,
                    json=final_payload,
                    params=final_params
                )

            if not response.ok:
                classes_logger.error(f'status code {response.status_code} from {method} {response.url}: {response.json()}')
                return response
            else:
                return response

        except Exception as e:
            classes_logger.error(f'ERROR CALLING {url}: {e}')
