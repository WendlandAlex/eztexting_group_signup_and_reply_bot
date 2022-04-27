from SmsTextingBase import SmsTextingBase, Contact, Group, Folder, IncomingMessage, SmsTextingError
import xml.etree.ElementTree as ET

class SmsTextingXML(SmsTextingBase):
    def __init__(self, base_url, login, password):
        SmsTextingBase.__init__(self, base_url, login, password)

    def _get(self,url, **params):
        params['format'] = 'xml'
        return SmsTextingBase._get(self,url, **params)

    def _update_post_url(self, url):
        return url + (url.find('?')==-1 and '?' or '&') + 'format=xml'

    def _parse_contacts_result(self, content):
        doc = ET.XML(content)
        res = []
        for entry in doc.findall('Entries/Entry'):
             contact = Contact(entry.findtext('PhoneNumber'), entry.findtext('FirstName'), entry.findtext('LastName'), entry.findtext('Email'), entry.findtext('Note'), map(getText, entry.findall('Groups/Group')), entry.findtext('Source'), entry.findtext('CreatedAt'), entry.findtext('ID'))
             res.append(contact)
        return res

    def _parse_contact_result(self, content):
        doc = ET.XML(content)
        entry = doc.find('Entry')
        return Contact(entry.findtext('PhoneNumber'), entry.findtext('FirstName'), entry.findtext('LastName'), entry.findtext('Email'), entry.findtext('Note'), map(getText, entry.findall('Groups/Group')), entry.findtext('Source'), entry.findtext('CreatedAt'), entry.findtext('ID'))

    def _parse_group_result(self, content):
        doc = ET.XML(content)
        entry = doc.find('Entry')
        return self._build_group(entry)

    def _parse_groups_result(self, content):
        doc = ET.XML(content)
        res = []
        for entry in doc.findall('Entries/Entry'):
             res.append( self._build_group(entry) )
        return res

    def _build_group(self, entry):
        return Group(entry.findtext('Name'), entry.findtext('Note'), entry.findtext('ContactCount'), entry.findtext('ID'))

    def _parse_folder_result(self, content):
        doc = ET.XML(content)
        entry = doc.find('Entry')
        return self._build_folder(entry)

    def _parse_folders_result(self, content):
        doc = ET.XML(content)
        res = []
        for entry in doc.findall('Entries/Entry'):
             res.append( self._build_folder(entry) )
        return res

    def _build_folder(self, entry):
        return Folder(entry.findtext('Name'), entry.findtext('ID'))

    def _parse_message_result(self, content):
        doc = ET.XML(content)
        entry = doc.find('Entry')
        return self._build_message(entry)

    def _parse_messages_result(self, content):
        doc = ET.XML(content)
        res = []
        for entry in doc.findall('Entries/Entry'):
             res.append( self._build_message(entry) )
        return res

    def _build_message(self, entry):
        return IncomingMessage(entry.findtext('PhoneNumber'), entry.findtext('Subject'), entry.findtext('Message'), entry.findtext('New'), entry.findtext('FolderID'), entry.findtext('ContactID'), entry.findtext('ReceivedOn'), entry.findtext('ID'))


    def _parse_errors(self, errcode, content):
        doc = ET.XML(content)
        return SmsTextingError(errcode, map(getText, doc.findall('Errors/Error')))

def getText(x): return x.text
