import requests
import json

from Classes.Superclass import Client
from Classes.Subclass import Contact

def get_all_contacts(client: Client, sorting=None, pagination=None):
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

def get_filtered_contacts(client: Client, filters_dict: dict=None, sort_by: str=None, sort_direction: str=None, paging_page_size: int=None, paging_page: int=None):
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
    