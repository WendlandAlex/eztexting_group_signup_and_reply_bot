import time
import datetime

from Classes import Client, Contact, Group, Message

def _strftime_unix(timestamp: datetime.datetime):
    timetuple = timestamp.timetuple()
    return time.mktime(timetuple)

def send_message(message_client: Client):
    pass

def receive_message():
    pass

def schedule_message(message_client: Client, datetime_object):
    sender = Message(message_client,
        StampToSend= _strftime_unix(datetime_object)
    )

    return sender.send_message()
