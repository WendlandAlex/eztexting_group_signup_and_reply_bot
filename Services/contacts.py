from __future__ import annotations
from typing import TYPE_CHECKING
TYPE_CHECKING = True

if TYPE_CHECKING:
    from Classes.Superclass import Client
    from Classes.Subclass import Contact
    from Services.groups import get_groupIds_from_names

import requests
import json
import os
import logging
logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


def get_all_contacts(client: "Client", sorting=None, pagination=None):
    """
    available sorting {
        "sortBy": "PhoneNumber"|"FirstName"|"LastName"|"CreatedAt"|"UpdatedAt",
        "sortDir": "asc"|"desc"
    }

    available pagination {
        "itemsPerPage": default=10,
        "page": variable
    }
    """
    query_params_dict = client.base_params_dict

    for kwarg in [sorting, pagination]:
        if kwarg is not None: query_params_dict.update(kwarg)

    response = client.make_api_call(
        url=f'{client.base_url}/contacts',
        method='GET',
        params_dict=query_params_dict
    )

    return [Contact(contact.get('ID')) for contact in response]

def get_filtered_contacts(client: "Client", filters_dict: dict=None, sort_by: str=None, sort_direction: str=None, paging_page_size: int=None, paging_page: int=None):
    """available filters {
        "filters[email][like]": "email",
        "filters[firstName][like]": "firstName",
        "filters[groupName][like]": "groupName",
        "filters[lastName][like]": "lastName",
        "filters[optOut][eq]": True|False,
        "filters[phoneNumber][like]": "phoneNumber",
        "filters[source][eq]": "Unknown"|"Webinterface"|"Upload"|"WebWidget"|"API"|"Keyword"
    }

    available sorting {
        "size": 10|20|50|100|200
    }

    available pagination {
        "sort": "{fieldName},{"asc"|"desc"}"
    }
    """
    query_params_dict = {}
    for k, v in filters_dict.items():
        if k in ['email', 'firstName', 'groupName', 'lastName', 'phoneNumber']:
            pass
        elif k in ['optOut', 'source']:
            query_params_dict.update({k: v})

    response = client.make_api_call(
        url=f'{client.base_url}/contacts',
        method='GET',
        params_dict=query_params_dict
    )

    return [Contact(contact.get('ID')) for contact in response]

def create_or_update_batch_of_contacts(client: "Client", contacts: list=None):
    for i in contacts:
        return i.__dict__
    
def modify_group_membership_of_contact(contact: "Contact", groupNames):
    groupIds = get_groupIds_from_names(client=contact._super, groupNames=groupNames)
    contact.groupIdsAdd = groupIds
    _logger.info(f'added contact {contact.phoneNumber} to the following groups: {contact.groupIdsAdd}')
    json_data = {"phoneNumber": contact.phoneNumber, "groupIds": contact.groupIdsAdd}

    response = requests.Request(
        method='POST',
        url='https://eztexting_api_endpoint.com',
        headers={'X-Authorization': 'Bearer oauthgoeshere'},
        json=json_data
    )

    response = response.prepare()

    if os.getenv('DEBUG', None):
        return response

    return True