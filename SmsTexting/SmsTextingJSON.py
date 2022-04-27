from SmsTextingBase import SmsTextingBase, Contact, Group, Folder, IncomingMessage, SmsTextingError
import simplejson as json

class SmsTextingJSON(SmsTextingBase):
    def __init__(self, base_url, login, password):
        SmsTextingBase.__init__(self, base_url, login, password)

    def _get(self,url, **params):
        params['format'] = 'json'
        return SmsTextingBase._get(self,url, **params)

    def _update_post_url(self, url):
        return url + (url.find('?')==-1 and '?' or '&') + 'format=json'

    def _parse_contacts_result(self, content):
        pyobj = json.loads(content)
        res = []
        for entry in pyobj['Response']['Entries']:
             contact = Contact(str(entry['PhoneNumber']), str(entry['FirstName']), str(entry['LastName']), str(entry['Email']), str(entry['Note']), entry['Groups'], str(entry['Source']), str(entry['CreatedAt']), str(entry['ID']))
             res.append(contact)
        return res

    def _parse_contact_result(self, content):
        pyobj = json.loads(content)
        entry = pyobj['Response']['Entry']
        return Contact(str(entry['PhoneNumber']), str(entry['FirstName']), str(entry['LastName']), str(entry['Email']), str(entry['Note']), entry['Groups'], str(entry['Source']), str(entry['CreatedAt']), str(entry['ID']))

    def _parse_group_result(self, content):
        pyobj = json.loads(content)
        entry = pyobj['Response']['Entry']
        return self._build_group(entry)

    def _parse_groups_result(self, content):
        pyobj = json.loads(content)
        res = []
        for entry in pyobj['Response']['Entries']:
             res.append( self._build_group(entry) )
        return res

    def _build_group(self, entry):
        return Group(str(entry['Name']), str(entry['Note']), entry['ContactCount'], str(entry['ID']))


    def _parse_folder_result(self, content):
        pyobj = json.loads(content)
        entry = pyobj['Response']['Entry']
        return self._build_folder(entry)

    def _parse_folders_result(self, content):
        pyobj = json.loads(content)
        res = []
        for entry in pyobj['Response']['Entries']:
             res.append( self._build_folder(entry) )
        return res

    def _build_folder(self, entry):
        return Folder(str(entry.get('Name', None)), str(entry.get('ID', None)))

    def _parse_message_result(self, content):
        pyobj = json.loads(content)
        entry = pyobj['Response']['Entry']
        return self._build_message(entry)

    def _parse_messages_result(self, content):
        pyobj = json.loads(content)
        res = []
        for entry in pyobj['Response']['Entries']:
             res.append( self._build_message(entry) )
        return res

    def _build_message(self, entry):
        return IncomingMessage(str(entry['PhoneNumber']), str(entry['Subject']), str(entry['Message']), str(entry['New']), str(entry['FolderID']), str(entry['ContactID']), str(entry['ReceivedOn']), str(entry['ID']))


    def _parse_errors(self, errcode, content):
        pyobj = json.loads(content)
        return SmsTextingError(errcode, pyobj['Response']['Errors'])