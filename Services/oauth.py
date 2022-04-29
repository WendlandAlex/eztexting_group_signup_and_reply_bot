import requests
import datetime
from logging import Logger


from Classes import Client

def generate_oauth_token(token_client: Client, appKey, appSecret):
    response = Client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/create',
        headers_dict=token_client.headers,
        payload_dict={'appKey': appKey, 'appSecret': appSecret}
        )

    accessToken = response.json().get('accessToken')
    refreshToken = response.json().get('refreshToken')
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=response.json().get('expiresInSeconds'))

    return accessToken, refreshToken, expiration_datetime

def refresh_oauth_token(token_client: Client, oauth_refresh_token):
    response = Client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/refresh',
        headers_dict=token_client.headers,
        payload_dict={'refreshToken': oauth_refresh_token}
        )

    accessToken = response.json().get('accessToken')
    refreshToken = response.json().get('refreshToken')
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=response.json().get('expiresInSeconds'))

    return accessToken, refreshToken, expiration_datetime

def revoke_oauth_token(token_client: Client, appKey, appSecret):
    response = Client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/revoke',
        headers_dict=token_client.headers,
        payload_dict={'appKey': appKey, 'appSecret': appSecret}
        )

    if response.ok:
        return True