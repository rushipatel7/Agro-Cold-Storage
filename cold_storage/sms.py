from django.http import HttpResponse
from twilio.rest import Client

def broadcast_sms():
    # message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                # "yet? Grab it here: https://www.twilio.com/quest")

    message_to_broadcast = ("Hiii")

    account_sid = 'AC7e092435f515ede4d0b8dbd1f4c4faa9'

    auth_token = '5cfd04bb3df4a92d615e1654341d60dd'


    client = Client(account_sid, auth_token)
    # for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
    #     if recipient:
    #         client.messages.create(to=recipient,
    #                                from_=settings.TWILIO_NUMBER,
    #                                body=message_to_broadcast)

    sms = client.messages.create(body=message_to_broadcast,
                                to='+919106016105',
                                from_= '+12019928044',)
                                # from_= '+12019928044',) //original number
    print("send successfully" ,sms)

# broadcast_sms()


def broadcast_sms1():
    # message_to_broadcast = ("Have you played the incredible TwilioQuest "
                                                # "yet? Grab it here: https://www.twilio.com/quest")

    message_to_broadcast = ("Hiii")

    account_sid = 'AC803f4d5bcef1ad59a96501703eaf8f3f'

    auth_token = '610297f40abbb78c37b6f000858b5b66'


    client = Client(account_sid, auth_token)
    # for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
    #     if recipient:
    #         client.messages.create(to=recipient,
    #                                from_=settings.TWILIO_NUMBER,
    #                                body=message_to_broadcast)

    sms = client.messages.create(body=message_to_broadcast,
                                to='+917046613313',
                                from_= '+18102558277',)
    print("send successfully" ,sms)

broadcast_sms1()