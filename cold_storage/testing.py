# Download the Python helper library from twilio.com/docs/python/install 
from twilio.rest import Client
from supply_chain_management import settings

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC7e092435f515ede4d0b8dbd1f4c4faa9"
auth_token  = "5cfd04bb3df4a92d615e1654341d60dd"
client = Client(account_sid, auth_token)

to_mobile_num = '+919106016105'
message = client.messages.create(
    body="Jenny please?! I love you <3",
    to=to_mobile_num,
    from_=settings.TWILIO_NUMBER)
print( message.sid)