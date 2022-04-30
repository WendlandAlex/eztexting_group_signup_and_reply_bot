from Classes.Superclass import Client

class Contact(Client):
    def __init__(self, superclass, phoneNumber: str=None, email: str=None, firstName: str=None, lastName: str=None, groupIdsAdd: list=None, groupIdsRemove: list=None, note: str=None, ):
        self.url=f'{self.base_url}/contacts'
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass
        
        self.phoneNumber        = phoneNumber
        self.email              = email
        self.firstName          = firstName
        self.lastName           = lastName
        self.groupIdsAdd        = groupIdsAdd
        self.groupIdsRemove     = groupIdsRemove
        self.note               = note

        data = self.get()
        if data is not None:
            for field, value in data.json().items():
                setattr(self, field, value)

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)

    def get(self):
        return self.make_api_call(
            url = self.url,
            method = 'GET',
            payload_dict={'phoneNumber': self.phoneNumber}
        )


class Folder(Client):
    def __init__(self, superclass):
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)


class Group(Client):
    def __init__(self, superclass):
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)


class Inbox(Client):
    def __init__(self, superclass):
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)


class Keyword(Client):
    def __init__(self, superclass):
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass
    
    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)


class MediaFile(Client):
    def __init__(self, superclass):
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)


class Message(Client):
    def __init__(self, superclass, fromNumber: str=None, groupIds: list=None, mediaFileId: str=None, mediaUrl: str=None, message: str=None, messageTemplateId: str=None, sendAt: str=None, strictValidation: bool=False, toNumbers: list=None, headers: dict=None):
        # we override __getattr__ so that the Message class dynamically pulls in attributes from Client
        # there are some attributes (e.g., accessToken that can refresh) that may need to change between sending multiple messages in a session
        # explanation here: https://stackoverflow.com/questions/1081253/inheriting-from-instance-in-python/1081925#1081925
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass
        # see definition of __getattr__ below
        # when the __init__ method runs during construction,
        # __getattr__ when called by self.{attr} will try to get it from the parent class, if it is defined in _super_attrs 

        # params of the message itself (from eztexting documentation: https://developers.eztexting.com/reference/createusingpost_3-1)
        self.companyName        = self.companyName
        self.fromNumber         = fromNumber
        self.groupIds           = groupIds
        self.mediaFileId        = mediaFileId
        self.mediaUrl           = mediaUrl
        self.message            = message
        self.messageTemplateId  = messageTemplateId
        self.sendAt             = sendAt
        self.strictValidation   = strictValidation # if one number in the list is invalid, no messages will be sent (including to valid numbers)
        self.toNumbers          = toNumbers

        # params we need to make the API call
        self.url                = f'{self.base_url}/messages'
        self.headers            = self.headers
        self.payload            = self.payload
        self.accessToken        = self.accessToken
        self.refreshToken       = self.refreshToken

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)

    def _load_payload(self):
        final_payload_dict = {}
        for i in ['fromNumber', 'groupIds', 'mediaFileId', 'mediaUrl', 'message', 'messageTemplateId', 'sendAt', 'strictValidation', 'toNumbers']:
            final_payload_dict[i] = self.__getattr__(i)

        return final_payload_dict

    def send(self):
        response = self.make_api_call(
            url = self.url,
            method = 'POST',
            headers_dict = self.headers,
            payload_dict = self._load_payload()
        )

        if response.status_code in [200, 201]:
            return response
