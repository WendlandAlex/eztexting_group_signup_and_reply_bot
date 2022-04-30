import requests
import datetime
from logging import Logger

def generate_oauth_token(token_client, appKey, appSecret):
    # response = token_client.make_api_call(
    #     method='POST',
    #     url=f'{token_client.base_url}/tokens/create',
    #     headers_dict=token_client.headers,
    #     payload_dict={'appKey': appKey, 'appSecret': appSecret},
    #     auth_method='http_basic'
    #     ).json()

    # print(response)

    response = {'accessToken': 'mytoken', 'refreshToken': 'mytoken', 'expiresInSeconds': '5400'}

    accessToken = response.get('accessToken')
    refreshToken = response.get('refreshToken')
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=int(response.get('expiresInSeconds')))

    return accessToken, refreshToken, expiration_datetime

def refresh_oauth_token(token_client, oauth_refresh_token):
    response = token_client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/refresh',
        headers_dict=token_client.headers,
        payload_dict={'refreshToken': oauth_refresh_token}
        )

    accessToken = response.json().get('accessToken')
    refreshToken = response.json().get('refreshToken')
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=response.json().get('expiresInSeconds'))

    return accessToken, refreshToken, expiration_datetime

def revoke_oauth_token(token_client, appKey, appSecret):
    response = token_client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/revoke',
        headers_dict=token_client.headers,
        payload_dict={'appKey': appKey, 'appSecret': appSecret}
        )

    if response.ok:
        return True