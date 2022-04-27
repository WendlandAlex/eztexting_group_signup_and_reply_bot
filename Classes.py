import requests
from logging import Logger

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
        try:
            new_params_dict = self.base_params_dict.update(params_dict)
            
            response =  requests.request(
                    verb=method,
                    url=url,
                    params=new_params_dict
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
        if self._get_contact():
            for field, value in self._get_contact.items():
                setattr(self, field, value)

    def _create_contact(self, new_params_dict):
        return super().make_api_call(
            url = self.url,
            method = 'GET',
            params_dict=new_params_dict
        ).get('data').get('Response').get('Entry')

    def _get_contact(self):
        return super().make_api_call(
            url = f'{self.url}/{self.contact_id}',
            method = 'GET'
        ).get('data').get('Response').get('Entry')

    def _update_contact(self, new_params_dict):
        """
        The only intended use case for this method is to immediately precede deleting the class instance
        So expect that any service calling this method will accept the return object and call 'del old_object'
        """
        response = super().make_api_call(
            url = f'{self.url}/{self.contact_id}',
            method = 'GET',
            params_dict=new_params_dict
        ).get('data').get('Response').get('Entry')

        return Contact(response.get('ID'))

    def _delete_contact(self):
        response = super().make_api_call(
            url = f'{self.url}/{self.contact_id}',
            method = 'DELETE'
        )

        if response.get('status_code') == 204:
            return True


class CreditCard(Client):
    def __init__(self, last_four_digits):
        self.url=f'{self.base_url}/billing/credits'
        if last_four_digits is not None: self.last_four_digits = last_four_digits
        credits_data = self._get_available_credits()
        self.TotalCredits = credits_data.get('TotalCredits')
        self.PlanCredits = credits_data.get('PlanCredits')
        self.AnytimeCredits = credits_data.get('AnytimeCredits')
        
    def _get_available_credits(self):
        return super().make_api_call(
            url = f'{self.url}/get',
            method = 'GET'
        ).get('data').get('Response').get('Entry')

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