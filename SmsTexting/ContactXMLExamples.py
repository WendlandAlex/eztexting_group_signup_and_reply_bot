import SmsTextingXML as SmsTexting

sms = SmsTexting.SmsTextingXML("https://app.eztexting.com", "smsdemo", "password")


try:
    print 'get_all_contacts'
    print sms.get_all_contacts(group='Honey Lovers')
    print

    contact = SmsTexting.Contact('2123456796', 'Piglet', 'P.', 'piglet@small-animals-alliance.org', 'It is hard to be brave, when you are only a Very Small Animal.')
    contact = sms.create_contact(contact)
    print 'create_contact: ' + str(contact)

    contact = sms.get_contact_by_id(contact.id)
    print 'get_contact_by_id: ' + str(contact)

    contact.groups=['Friends', 'Neighbors']
    contact = sms.update_contact(contact)
    print 'update_contact: ' + str(contact)

    print 'delete.'
    sms.delete_contact(contact.id)

    print 'second delete. try to get error'
    sms.delete_contact(contact.id)

except SmsTexting.SmsTextingError, error:
    print str(error)