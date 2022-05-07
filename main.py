from __future__ import annotations
from typing import TYPE_CHECKING
from flask import Flask, abort, request, Response
import dotenv
import os
import json
import logging
logging.getLogger('asyncio').setLevel(logging.WARNING)


TYPE_CHECKING = True
if TYPE_CHECKING:
    from Classes.Superclass             import Client
    from Classes.Subclass               import Contact, Folder, Group, Inbox, Keyword, MediaFile, Message
    from Services.contacts              import get_all_contacts, get_filtered_contacts, create_or_update_batch_of_contacts, modify_group_membership_of_contact
    from Services.messages              import regex_parse_message_body
    from Handlers.inbound_text_received import send_confirmation
    from Handlers.keyword_opt_in        import *
    from Handlers.admin_commands        import *
    from Handlers.validators            import validate_hash_from_header

dotenv.load_dotenv()

eztexting_username                  = os.getenv('EZTEXTING_USERNAME')
eztexting_password                  = os.getenv('EZTEXTING_PASSWORD')
eztexting_companyName               = os.getenv('COMPANY_NAME', 'test company')
eztexting_creditcard_number         = os.getenv('EZTEXTING_CREDITCARD', None)
eztexting_admin_phone_number        = os.getenv('EZTEXTING_ADMIN_PHONE_NUMBER', None)
inbound_phone_number                = os.getenv('INBOUND_PHONE_NUMBER', None)
base_url                            = os.getenv('BASE_URL', 'https://a.eztexting.com/v1')
webhook_secret_key                  = os.getenv('WEBHOOK_SECRET_KEY', None)
webhook_url                         = os.getenv('WEBHOOK_URL', None)
oauth_token_server_url              = os.getenv('OAUTH_TOKEN_SERVER_URL', 'http://127.0.0.1:8888/generate_token')
oauth_token_server_shared_secret    = os.getenv('OAUTH_TOKEN_SERVER_SHARED_SECRET', None)
DEBUG                               = os.getenv('DEBUG', False)

eztexting_client            = Client(eztexting_username, eztexting_password, eztexting_companyName, base_url, oauth_token_server_url=oauth_token_server_url)

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

async def dispatch_task(fromNumber=None, message=None):
    send_confirmation_response = None
    message = message.lower()
    sending_contact = Contact(eztexting_client, phoneNumber=fromNumber)

    groupNames = regex_parse_message_body(message, fromNumber, queue=False)
    if groupNames is not None:
        if modify_group_membership_of_contact(sending_contact, groupNames): 
            send_confirmation_response = send_confirmation(sending_contact, groupNames, queue=False)

    if send_confirmation_response is not None:
        return send_confirmation_response
    else:
        return Response(json.dumps({'message': 'No valid signup group provided'}), status=404)

# setup flask webhook handler #
app = Flask(__name__)

@app.route('/inbound_text_received', methods=['POST'])
async def handle_sms():
    try:
        message_type = request.json.get('type', None)

        if message_type != 'inbound_text.received':
            abort(404)
    except Exception as e:
        print(e)
        abort(400)

    if not validate_hash_from_header(request.headers.get('X-Signature'), request.json, webhook_secret_key):
        abort(403)

    return await dispatch_task(fromNumber=request.json.get('fromNumber'), message=request.json.get('message'))
    
if __name__ == '__main__':
    main()
    app.run(port=8080)
