import requests
import json

from Classes import Client, Contact

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

def get_filtered_contacts(client: Client, filters_dict, sorting=None, pagination=None):
    """available filters {
        "query": FirstName|LastName|PhoneNumber,
        "source": "Unknown"|"Manually Added"|"Upload"|"Web Widget"|"API"|"Keyboard",
        "optout": "true"|"false"
        "group": name_of_group
    }

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

    for kwarg in [filters_dict, sorting, pagination]:
        if kwarg is not None: query_params_dict.update(kwarg)

    response = client.make_api_call(
        url=f'{client.base_url}/contacts',
        method='GET',
        params_dict=query_params_dict
    )

    return [Contact(contact.get('ID')) for contact in response]
    