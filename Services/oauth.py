from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Superclass import Client

import datetime
from logging import Logger

def generate_oauth_token_pair(token_client: "Client"):
    response = token_client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/create',
        headers_dict=token_client.headers,
        payload_dict={'appKey': token_client.username, 'appSecret': token_client.password},
        auth_method=None
        ).json()

    # response = {'accessToken': 'mytoken', 'refreshToken': 'mytoken', 'expiresInSeconds': '5400'}

    accessToken = response.get('accessToken')
    refreshToken = response.get('refreshToken')
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=int(response.get('expiresInSeconds')))

    return accessToken, refreshToken, expiration_datetime

def refresh_oauth_token_pair(token_client: "Client"):
    response = token_client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/refresh',
        headers_dict=token_client.headers,
        payload_dict={'refreshToken': token_client.refreshToken}
        )

    accessToken = response.json().get('accessToken')
    refreshToken = response.json().get('refreshToken')
    expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=response.json().get('expiresInSeconds'))

    return accessToken, refreshToken, expiration_datetime

def revoke_oauth_access_token(token_client: "Client"):
    response = token_client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/revoke',
        headers_dict=token_client.headers,
        payload_dict={'token': token_client.accessToken, 'type': "ACCESS_TOKEN"}
        )

    if response.ok:
        return True

def revoke_oauth_refresh_token(token_client: "Client"):
    response = token_client.make_api_call(
        method='POST',
        url=f'{token_client.base_url}/tokens/revoke',
        headers_dict=token_client.headers,
        payload_dict={'token': token_client.refreshToken, 'type': "REFRESH_TOKEN"}
        )

    if response.ok:
        return True