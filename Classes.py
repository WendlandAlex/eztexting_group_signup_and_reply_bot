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
            query_params_dict = self.base_params_dict.update(params_dict)
            
            response =  requests.request(
                    verb=method,
                    url=url,
                    params=query_params_dict
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

    def create_contact(self, query_params_dict):
        return super().make_api_call(
            url = self.url,
            method = 'GET',
            params_dict=query_params_dict
        ).get('data').get('Response').get('Entry')

    def update_contact(self, query_params_dict):
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

    def delete_contact(self):
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
    def __init__(self, PhoneNumbers, Message, Groups=None, Subject=None, StampToSend=None, MessageTypeID=None, FileID=None):
        self.url            = f'{self.base_url}/messages'
        self.PhoneNumbers   = PhoneNumbers
        self.Groups         = Groups
        self.Subject        = Subject
        self.Message        = Message
        self.StampToSend    = StampToSend
        self.MessageTypeID  = MessageTypeID
        self.FileID         = FileID
        
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