from Classes.Superclass import Client
import os

class Contact(Client):
    _payload_attrs = ['phoneNumber', 'email', 'firstName', 'lastName', 'groupIdsAdd', 'groupIdsRemove', 'note', 'custom1', 'custom2', 'custom3', 'custom4', 'custom5']

    def __init__(self, superclass, phoneNumber: str=None, email: str=None, firstName: str=None, lastName: str=None, groupIdsAdd: list=None, groupIdsRemove: list=None, note: str=None, custom1=None, custom2=None, custom3=None, custom4=None, custom5=None):
        self._super = superclass
        self._super_attrs = self._attrs_for_subclass # duplicate the parent variable here, to aid readbility in later functions
        self.url=f'{self.base_url}/contacts'

        self.phoneNumber        = phoneNumber
        self.email              = email
        self.firstName          = firstName
        self.lastName           = lastName
        self.groupIdsAdd        = groupIdsAdd # Is groupIdsAdd idempotent? Do we care about losing metadata like length of group membership if we always overwrite on update?
        self.groupIdsRemove     = groupIdsRemove
        self.note               = note
        self.custom1            = custom1
        self.custom2            = custom2
        self.custom3            = custom3
        self.custom4            = custom4
        self.custom5            = custom5

        if not os.getenv('DEBUG', None):
            if self.phoneNumber is not None:
                try:
                    data = self.get()
                    if data is not None:
                        for field, value in data.json().items():
                            setattr(self, field, value)
            
                # TODO: find out return when contact doesn't exist yet 
                except:
                    pass

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
            url = self.url + f'/{self.phoneNumber}',
            method = 'GET',
            payload_dict={'phoneNumber': self.phoneNumber}
        )

    def delete(self):
        return self.make_api_call(
            url = self.url + f'/{self.phoneNumber}',
            method = 'DELETE'
        )

    def create_or_update(self):
        return self.make_api_call(
            url = self.url,
            method = 'POST',
            payload_dict=self._finalize_payload()
        )

    def _finalize_payload(self):
        final_payload_dict = {}
        for i in self._payload_attrs:
            final_payload_dict[i] = self.__getattr__(i)

        return final_payload_dict



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
    def __init__(self, superclass, groupId=None, groupName=None):
        self._super = superclass
        self._super_attrs = self._super._attrs_for_subclass
        self.groupId = groupId
        self.groupName = groupName

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
    _payload_attrs = ['fromNumber', 'groupIds', 'mediaFileId', 'mediaUrl', 'message', 'messageTemplateId', 'sendAt', 'strictValidation', 'toNumbers']

    def __init__(self, superclass, fromNumber: str=None, groupIds: list=None, mediaFileId: str=None, mediaUrl: str=None, message: str=None, messageTemplateId: str=None, sendAt: str=None, strictValidation: bool=False, toNumbers: list=None, headers: dict=None):
        # we override __getattr__ so that the Message class dynamically pulls in attributes from Client
        # there are some attributes (e.g., accessToken that can refresh) that may need to change between sending multiple messages in a session
        # explanation here: https://stackoverflow.com/questions/1081253/inheriting-from-instance-in-python/1081925#1081925
        self._super = superclass
        self._super_attrs = self._attrs_for_subclass
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

    def __getattr__(self, attr, attr_if_attr_not_in_super=None):
        if attr in self._super_attrs:
            try:
                return getattr(self._super, attr)
            except AttributeError:
                return attr_if_attr_not_in_super

        # non-override version (for non-parent attributes)
        else: return self.__dict__.get(attr)

    def _finalize_payload(self):
        final_payload_dict = {}
        for payload_attr_iterator in self._payload_attrs:
            if payload_attr_iterator is not None:
                final_payload_dict[payload_attr_iterator] = self.__getattr__(payload_attr_iterator)

        return final_payload_dict

    def send(self):
        response = self.make_api_call(
            url = self.url,
            method = 'POST',
            headers_dict = self.headers,
            payload_dict = self._finalize_payload()
        )

        if response.status_code in [200, 201]:
            return response
