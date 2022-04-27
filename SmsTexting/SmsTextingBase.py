import urllib, urllib2

class SmsTextingBase:
    def __init__(self, base_url, login, password):
        self.base_url = base_url
        self.login = login
        self.password = password

    def _prepare_params(self, **params):
        #remove empty params
        keys = params.keys()
        for k in keys: 
            if params[k] is None: del params[k]
            elif getattr(params[k], '__iter__', False):
                for i, item in enumerate(params[k]):
                    params[k+'['+str(i)+']']=item
                del params[k]
        params['User'] = self.login
        params['Password'] = self.password
        return urllib.urlencode(params)

    def _get(self,url, **params):
        str_params = self._prepare_params(**params)
        try:
            resp = urllib2.urlopen(self.base_url+ url + '?' + str_params)
            return resp.read()
        except urllib2.HTTPError, error:
            raise self._parse_errors(error.code, error.read())

    def _update_post_url(self, url):
        """ to be redefined in subclasses
        """
        return url

    def _post(self,url, **params):
        str_params = self._prepare_params(**params)
        return self._post2(url, str_params)

    def _post2(self,url, str_params):
        url = self._update_post_url(url)
        try:
            resp = urllib2.urlopen(self.base_url+ url, str_params)
            return resp.read()
        except urllib2.HTTPError, error:
            if error.code == 201: #actually, this is success
                return error.read()
            elif error.code == 204: #actually, this is success
                return error.read()
            else:
                raise self._parse_errors(error.code, error.read())

    def _delete(self,url, **params):
        self._post(url+'?_method=DELETE', **params)

    def get_all_contacts(self, query=None, source=None, optout=None, group=None, sortBy=None, sortDir=None, itemsPerPage=None, page=None):
        """Get a list of contacts stored in your Ez Texting contact list.

        Filters
        query (Optional) Search contacts by first name / last name / phone number
        source (Optional) Source of contacts. Available values: 'Unknown', 'Manually Added', 'Upload', 'Web Widget', 'API', 'Keyword'
        optout (Optional) Opted out / opted in contacts. Available values: true, false.
        group (Optional) Name of the group the contacts belong to
        Sorting
        sortBy (Optional) Property to sort by. Available values: PhoneNumber, FirstName, LastName, CreatedAt
        sortDir (Optional) Direction of sorting. Available values: asc, desc
        Pagination
        itemsPerPage (Optional) Number of results to retrieve. By default, 10 most recently added contacts are retrieved.
        page (Optional) Page of results to retrieve

        result - list of contact objects
        """
        res = self._get("/contacts",  query=query, source=source, optout=optout, group=group, sortBy=sortBy, sortDir=sortDir, itemsPerPage=itemsPerPage, page=page)
        return self._parse_contacts_result(res)

    def get_contact_by_id(self, id):
        """Get a single contact stored in your Ez Texting contact list.
        """
        res = self._get("/contacts/"+id)
        return self._parse_contact_result(res)

    def delete_contact(self, id):
        """Delete a contact stored in your Ez Texting contact list.
        """
        self._delete("/contacts/"+id)

    def create_contact(self, contact):
        """Create a new contact that will be stored in your Ez Texting contact list.

           contact - Contact object. PhoneNumber is required, other fields are optional.
           returns contact object
        """
        res = self._post("/contacts", PhoneNumber=contact.phone_number, FirstName=contact.first_name, LastName=contact.last_name, Email=contact.email, Groups=contact.groups, Note=contact.note)
        return self._parse_contact_result(res)

    def update_contact(self, contact):
        """Update a contact stored in your Ez Texting contact list.

           contact - Contact object. id and PhoneNumber are required, other fields are optional.
           returns contact object
        """
        res = self._post("/contacts/"+contact.id, PhoneNumber=contact.phone_number, FirstName=contact.first_name, LastName=contact.last_name, Email=contact.email, Groups=contact.groups, Note=contact.note)
        return self._parse_contact_result(res)

    def get_all_groups(self, sortBy=None, sortDir=None, itemsPerPage=None, page=None):
        """Get a list of groups stored in your Ez Texting account.

        Sorting
        sortBy (Optional) Property to sort by. Available values: Name
        sortDir (Optional) Direction of sorting. Available values: asc, desc
        Pagination
        itemsPerPage (Optional) Number of results to retrieve. By default, first 10 groups sorted in alphabetical order are retrieved.
        page (Optional) Page of results to retrieve

        result - list of group objects
        """
        res = self._get("/groups",  sortBy=sortBy, sortDir=sortDir, itemsPerPage=itemsPerPage, page=page)
        return self._parse_groups_result(res)

    def get_group_by_id(self, id):
        """Get a single group stored in your Ez Texting group list.
        """
        res = self._get("/groups/"+id)
        return self._parse_group_result(res)

    def delete_group(self, id):
        """Delete a group stored in your Ez Texting account.
        """
        self._delete("/groups/"+id)

    def create_group(self, group):
        """Create a new group that will be stored in your Ez Texting account.

           group - group object. name is required, note is optional.
           returns group object
        """
        res = self._post("/groups", Name=group.name, Note=group.note)
        return self._parse_group_result(res)

    def update_group(self, group):
        """Update a group stored in your Ez Texting account.

           group - group object. id and name are required, note is optional.
           returns group object
        """
        res = self._post("/groups/"+group.id, Name=group.name, Note=group.note)
        return self._parse_group_result(res)

    def get_all_folders(self):
        """Get all Folders in your Ez Texting Inbox.

        result - list of folder objects
        """
        res = self._get("/messages-folders")
        return self._parse_folders_result(res)

    def get_folder_by_id(self, id):
        """Get a single folder in your Ez Texting Inbox.
        """
        res = self._get("/messages-folders/"+id)
        return self._parse_folder_result(res)

    def delete_folder(self, id):
        """Delete a Folder in your Ez Texting Inbox.
        """
        self._delete("/messages-folders/"+id)

    def create_folder(self, folder):
        """Create a Folder in your Ez Texting Inbox.

           folder - folder object. name is required.
           returns folder object
        """
        res = self._post("/messages-folders", Name=folder.name)
        return self._parse_folder_result(res)

    def update_folder(self, folder):
        """Update the name of a Folder in your Ez Texting Inbox.

           folder - folder object. id and name are required.
        """
        res = self._post("/messages-folders/"+folder.id, Name=folder.name)

    def get_all_messages(self, folder_id=None, search=None, sortBy=None, sortDir=None, itemsPerPage=None, page=None):
        """Get all incoming text messages in your Ez Texting Inbox.
        folder_id (Optional) Get messages from the selected folder. If FolderID is not given then request will return messages in your Inbox and all folders.
        search (Optional) Get messages which contain selected text or which are sent from selected phone number.
        Sorting
        sortBy (Optional) Property to sort by. Available values: ReceivedOn, PhoneNumber, Message
        sortDir (Optional) Direction of sorting. Available values: asc, desc
        Pagination
        itemsPerPage (Optional) Number of results to retrieve. By default, first 10 groups sorted in alphabetical order are retrieved.
        page (Optional) Page of results to retrieve

        result - list of message objects
        """
        res = self._get("/incoming-messages",  FolderID=folder_id, Search=search, sortBy=sortBy, sortDir=sortDir, itemsPerPage=itemsPerPage, page=page)
        return self._parse_messages_result(res)

    def get_message_by_id(self, id):
        """Get a single incoming text messages in your Ez Texting Inbox.
        """
        res = self._get("/incoming-messages/"+id)
        return self._parse_message_result(res)

    def delete_message(self, id):
        """Delete an incoming text message in your Ez Texting Inbox.
        """
        self._delete("/incoming-messages/"+id)

    def move_message_to_folder(self, ids, folder_id):
        """Moves an incoming text message in your Ez Texting Inbox to a specified folder. 
           Note: You may include multiple Message IDs to move multiple messages to same folder in a single API call.
        """
        str_params = self._prepare_params(FolderID=folder_id)
        if getattr(ids, '__iter__', False):
            for i, item in enumerate(ids):
                str_params = str_params + '&ID[]='+item
        else:
            str_params = str_params + '&ID='+ids
        self._post2("/incoming-messages/?_method=move-to-folder", str_params)



class SmsTextingError:
    def __init__(self, error_code, errors):
        self.error_code = error_code
        self.errors = errors
    def __str__(self):
       return 'Error code: ' + str(self.error_code) + \
              ', Errors description: ' + str(self.errors)
    def __repr__(self):
        return self.__str__()

class Contact:
    def __init__(self, phone_number, first_name=None, last_name=None, email=None, note=None, groups=None, source=None, created_at=None, id=None):
        self.id = id
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.note = note
        self.source = source
        self.groups = groups
        self.created_at = created_at

    def __str__(self):
       return 'Contact ID: ' + self.id + \
              ', Phone Number: ' + self.phone_number + \
              ', First Name: ' + self.first_name + \
              ', Last Name: ' + self.last_name + \
              ', Email: ' + self.email + \
              ', Note: ' + self.note + \
              ', Source: ' + self.source + \
              ', Groups: ' + str(self.groups) + \
              ', CreatedAt: ' + self.created_at
    def __repr__(self):
        return self.__str__()

class Group:
    def __init__(self, name, note=None, contacts_number=None, id=None):
        self.id = id
        self.name = name
        self.note = note
        self.contacts_number = contacts_number

    def __str__(self):
       return 'Group ID: ' + self.id + \
              ', Name: ' + self.name + \
              ', Note: ' + self.note + \
              ', Number of Contacts: ' + str(self.contacts_number)
    def __repr__(self):
        return self.__str__()

class Folder:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __str__(self):
       return 'Folder ID: ' + str(self.id) + \
              ', Name: ' + str(self.name)
    def __repr__(self):
        return self.__str__()

class IncomingMessage:
    def __init__(self, phone_number, subject, message, new, folder_id, contact_id, received_on=None, id=None):
        self.id = id
        self.phone_number = phone_number
        self.subject = subject
        self.message = message
        self.new = new
        self.folder_id = folder_id
        self.contact_id = contact_id
        self.received_on = received_on

    def __str__(self):
       return 'Message ID: ' + self.id + \
              ', Phone Number: ' + self.phone_number + \
              ', Subject: ' + self.subject + \
              ', Message: ' + self.message + \
              ', New: ' + self.new + \
              ', Folder ID: ' + self.folder_id + \
              ', Contact ID: ' + self.contact_id + \
              ', Received On: ' + self.received_on + '\n'
    def __repr__(self):
        return self.__str__()
