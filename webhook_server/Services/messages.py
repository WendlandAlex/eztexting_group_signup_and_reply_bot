from __future__ import annotations
from typing import TYPE_CHECKING
TYPE_CHECKING = True

if TYPE_CHECKING:
    from Classes.Superclass import Client
    from Classes.Subclass import Contact, Group, Message

import time
import datetime
import urllib
import re


def _strftime_unix(timestamp: datetime.datetime):
    # sanitize tzinfo and convert to epoch seconds in UTC
    # strip the decimal
    timetuple = timestamp.replace(tzinfo=datetime.timezone.utc).timetuple()
    return time.mktime(timetuple)

def regex_parse_message_body(message: str, fromNumber: str=None, id: str=None, queue=False):
    groupNames = []
    days_of_week_regex_pattern = re.compile('(mon|tues|wednes|thurs|fri|satur|sun)day', re.IGNORECASE)
    signup_day_matches = re.findall(days_of_week_regex_pattern, message)

    if len(signup_day_matches) > 0:
        for i in signup_day_matches:
            groupNames.append(f'{i}day')

        if len(groupNames) > 0:
            return groupNames

    else: return None
