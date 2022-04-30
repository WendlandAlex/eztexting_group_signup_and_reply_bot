import time
import datetime
import urllib

from Classes.Superclass import Client
from Classes.Subclass import Contact, Group, Message

def _strftime_unix(timestamp: datetime.datetime):
    # sanitize tzinfo and convert to epoch seconds in UTC
    # strip the decimal
    timetuple = timestamp.replace(tzinfo=datetime.timezone.utc).timetuple()
    return time.mktime(timetuple)

def send_message(message_client: Client):
    pass

def receive_inbox_message_reply(message: Message, phone_number, message_body):
    message_body = urllib.parse.unquote(message_body)


def receive_pointer_to_inbox_message():
    pass

def schedule_message(message_client: Client, datetime_object: datetime.datetime):
    sender = Message(message_client,
        StampToSend= _strftime_unix(datetime_object)
    )

    return sender.send()
