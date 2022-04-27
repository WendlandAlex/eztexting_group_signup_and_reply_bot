import requests
import os
import json

from Classes import Client, Contact, CreditCard, Folder, Group, Inbox, Keyword, Message
from Services import send, receive, scheduled_send, generate_credit_report

eztexting_username      = os.getenv('USERNAME')
eztexting_password      = os.getenv('PASSWORD')
eztexting_creditcard    = os.getenv('EZTEXTING_CREDITCARD')
eztexting_admin_contact = os.getenv('EZTEXTING_ADMIN_CONTACT')
base_url                = 'https://app.eztexting.com'

eztexting_client = Client(eztexting_username, eztexting_password, base_url)
eztexting_creditcard = CreditCard(eztexting_client, eztexting_creditcard)

def main():
    pass

if __name__ == '__main__':
    exit(main())
