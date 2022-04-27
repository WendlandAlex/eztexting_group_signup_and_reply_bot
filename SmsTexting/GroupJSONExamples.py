import SmsTextingJSON as SmsTexting

sms = SmsTexting.SmsTextingJSON("https://app.eztexting.com", "smsdemo", "password")


try:
    print 'get_all_groups'
    print sms.get_all_groups(sortBy='Name', sortDir='asc', itemsPerPage=10)
    print

    group = SmsTexting.Group('Tubby Bears', 'A bear, however hard he tries, grows tubby without exercise')
    group = sms.create_group(group)
    print 'create_group: ' + str(group)

    group = sms.get_group_by_id(group.id)
    print 'get_group_by_id: ' + str(group)

    group = sms.update_group(group)
    print 'update_group: ' + str(group)

    print 'delete.'
    sms.delete_group(group.id)

    print 'second delete. try to get error'
    sms.delete_group(group.id)

except SmsTexting.SmsTextingError, error:
    print str(error)