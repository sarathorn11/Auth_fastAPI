# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
def sms_sent(reset_code,phone_number):
    account_sid = "AC97b14b059cd77ff4bd48ee15cd0cf08b"
    auth_token = "b53fdd1b19a688bc3629fc94f9fce43d"
    client = Client(account_sid, auth_token)
    client.messages.create(
    body="Hello Sir/madim Someone have request a link reset your password. If you requested this,your code is "+ reset_code +" and you can change your password",
    from_="+15855493679",
    to=phone_number
    )
    return {'message': "Success"}