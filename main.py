import requests
import os
import json

from Classes import Contact, Credits, Folder, Group, Inbox, Keyword, Message
from Services import send, receive

eztexting_username      = os.getenv('USERNAME')
eztexting_password      = os.getenv('PASSWORD')
base_url                = 'https://app.eztexting.com'

def main():
    pass

if __name__ == '__main__':
    exit(main())
