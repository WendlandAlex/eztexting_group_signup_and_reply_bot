from __future__ import annotations
from typing import TYPE_CHECKING
import dotenv
import os

TYPE_CHECKING = True
if TYPE_CHECKING:
    from Classes.Superclass import Client
    from Classes.Subclass import Contact, Folder, Group, Inbox, Keyword, MediaFile, Message
    from Services.contacts import get_all_contacts, get_filtered_contacts, create_or_update_batch_of_contacts
    from Services.messages import send_message, receive_inbox_message_reply, receive_pointer_to_inbox_message, schedule_message 
    from Handlers.inbound_text_received import *
    from Handlers.keyword_opt_in import *
    from Handlers.admin_commands import *

dotenv.load_dotenv()

eztexting_username              = os.getenv('EZTEXTING_USERNAME')
eztexting_password              = os.getenv('EZTEXTING_PASSWORD')
eztexting_companyName           = os.getenv('COMPANY_NAME', 'test company')
eztexting_creditcard_number     = os.getenv('EZTEXTING_CREDITCARD', None)
eztexting_admin_phone_number    = os.getenv('EZTEXTING_ADMIN_PHONE_NUMBER', None)
inbound_phone_number            = os.getenv('INBOUND_PHONE_NUMBER', None)
base_url                        = os.getenv('BASE_URL', 'https://a.eztexting.com/v1')

eztexting_client                = Client(eztexting_username, eztexting_password, eztexting_companyName, base_url)

def main():
    # print(
    #     Message(eztexting_client, fromNumber=inbound_phone_number).send()
    # )
    # print(
    #     eztexting_client
    # )
    print(
        Contact(eztexting_client, phoneNumber=eztexting_admin_phone_number, custom1="my super cool custom1").create_or_update()
    )

if __name__ == '__main__':
    exit(main())
