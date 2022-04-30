import requests
import dotenv
import os
import json

from Classes import Client, Contact, Folder, Group, Inbox, Keyword, MediaFile, Message
from Services.contacts import get_all_contacts, get_filtered_contacts
from Services.messages import send_message, receive_inbox_message_reply, receive_pointer_to_inbox_message, schedule_message 
from Handlers.inbox_message_replies import *
from Handlers.keyword_replies import *
from Handlers.admin_commands import *

dotenv.load_dotenv()

eztexting_username              = os.getenv('EZTEXTING_USERNAME')
eztexting_password              = os.getenv('EZTEXTING_PASSWORD')
eztexting_companyName           = os.getenv('COMPANY_NAME', 'say it with your chest dtx')
eztexting_creditcard_number     = os.getenv('EZTEXTING_CREDITCARD', None)
eztexting_admin_contact         = os.getenv('EZTEXTING_ADMIN_CONTACT', None)
base_url                        = os.getenv('BASE_URL', 'https://a.eztexting.com/v1')

eztexting_client                = Client(eztexting_username, eztexting_password, eztexting_companyName, base_url)
# eztexting_admin                 = Contact(eztexting_admin_contact)

def main():
    print(
        eztexting_client.__dict__
    )
if __name__ == '__main__':
    exit(main())