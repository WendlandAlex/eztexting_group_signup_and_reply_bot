import requests
import os
from Classes.Subclass import Group

debug_mapping = {
    'monday': '123123',
    'tuesday': '234234',
    'wednesday': '345345',
    'thursday': '456456',
    'friday': '567567',
    'saturday': '678678',
    'sunday': '789789'
}

def get_groupIds_from_names(client, groupNames):
    results = []
    for i in groupNames:
        group = Group(client, name=i)
        if os.getenv('DEBUG', False):
            group.id = debug_mapping.get(f'{group.name}')

        results.append(group.id)

    return results
