import base64
import datetime
import os
import requests
import pprint
import logging
logging.basicConfig(level=logging.DEBUG)
classes_logger = logging.getLogger(__name__)
if os.getenv('DEBUG', None):
    classes_logger.setLevel(logging.DEBUG)
classes_logger.setLevel(logging.ERROR)

from Services.oauth import generate_oauth_token_pair, refresh_oauth_token_pair, revoke_oauth_access_token, revoke_oauth_refresh_token

class Client():
    # identify the core set of attributes needed for all API calls
    # subclasses of API class can inherit these by overriding __getattr__ to call the superclass's attributes
    _attrs_for_subclass = ['companyName', 'base_url', 'headers', 'payload', 'accessToken', 'refreshToken']

    def __init__(self, username=None, password=None, companyName=None, base_url=None, payload={}, headers={}, params=[]):
        self.payload = payload
        self.headers = headers
        self.params = params
        self.username = username
        self.password = password
        self.companyName = companyName
        self.base_url = base_url
        self._generate_or_refresh_oauth_token_pair()
        self._update_payload(**{"companyName": self.companyName})
        self._update_headers(**{"Accept": "*/*", "Content-Type": "application/json"})

    def __str__(self):
        return pprint.pformat(self.__dict__)

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

    def _generate_or_refresh_oauth_token_pair(self):
        if all(hasattr(self, attribute) for attribute in ['accessToken', 'refreshToken', 'expiration_datetime']):
            # refresh the token if it expires in the next 10 seconds
            if self.expiration_datetime < datetime.datetime.now() + datetime.timedelta(seconds=10):
                accessToken, refreshToken, expiration_datetime = refresh_oauth_token_pair(self, self.refreshToken)

                self.accessToken = accessToken
                self.refreshToken = refreshToken
                self.expiration_datetime = expiration_datetime

        else:
            accessToken, refreshToken, expiration_datetime = generate_oauth_token_pair(self)

            self.accessToken = accessToken
            self.refreshToken = refreshToken
            self.expiration_datetime = expiration_datetime

        return self

    def make_api_call(self, method, url, headers_dict: dict=None, payload_dict: dict=None, params_list_of_tuples: list=None, auth_method='oauth'):
        final_headers = self.headers.copy()
        final_payload = self.payload.copy()
        final_params  = self.params.copy()

        if auth_method == 'oauth':
            auth_header = {'Authorization': f'Bearer {self.accessToken}'}

        elif auth_method == 'http_basic':
            auth_string = ':'.join([self.username, self.password])
            b64_encoded_auth_string = base64.b64encode(auth_string.encode())
            auth_header = {'Authorization': f'Basic {b64_encoded_auth_string.decode()}'}

        else: auth_header = {}

        try:
            for headers_dict_iterator in [self.headers, headers_dict, auth_header]:
                if headers_dict_iterator is not None:
                    final_headers.update(headers_dict_iterator)

            for payload_dict_iterator in [self.payload, payload_dict]:
                if payload_dict_iterator is not None:
                    final_payload.update(payload_dict_iterator)

            # python requests may accept a dict of params
            # but this prevents duplicate values for same key
            # contact-group update requires a querystring of '?phoneNumbers=1&phoneNumbers=2'
            for params_list_of_tuples_iterator in [self.params, params_list_of_tuples]:
                if params_list_of_tuples_iterator is not None:
                    final_params.append(params_list_of_tuples_iterator)

            session = requests.Session()
            final_request =  requests.Request(
                    method=method,
                    url=url,
                    headers=final_headers,
                    json=final_payload,
                    params=final_params
                ).prepare()


            if os.getenv('DEBUG', None):
                classes_logger.debug({
                        "_sent_by_class": type(self).__qualname__,
                        "_called_with_args": locals(),
                        "url": final_request.url,
                        "method": final_request.method,
                        "payload": final_request.body,
                        "headers": final_request.headers
                        })

            response = session.send(final_request)

            if not response.ok:
                classes_logger.error(f'status code {response.status_code} from {method} {response.url}: {response.json()}')
                return response
            else:
                return response

        except Exception as e:
            classes_logger.error(f'ERROR CALLING {url}: {e}')
            raise
