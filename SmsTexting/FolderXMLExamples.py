import SmsTextingXML as SmsTexting

sms = SmsTexting.SmsTextingXML("https://app.eztexting.com", "demouser", "password")


try:
    print 'get_all_folders'
    print sms.get_all_folders()
    print

    folder = SmsTexting.Group('Customers')
    folder = sms.create_folder(folder)
    print 'create_folder: ' + str(folder)

    folder_id = folder.id

    folder = sms.get_folder_by_id(folder_id)
    print 'get_folder_by_id: ' + str(folder)

    print 'update_folder.'
    folder.id = folder_id
    folder.name = 'Customers2'
    sms.update_folder(folder)

    folder = sms.get_folder_by_id(folder_id)
    print 'get_folder_by_id: ' + str(folder)

    print 'delete.'
    sms.delete_folder(folder_id)

    print 'second delete. try to get error'
    sms.delete_folder(folder_id)

except SmsTexting.SmsTextingError, error:
    print str(error)