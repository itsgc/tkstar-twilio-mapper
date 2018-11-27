import os
import yaml
import utils

from twilio.rest import Client


settings = utils.make_settings('/home/karmik/tkstar-twilio-mapper/config.yml')

ACCOUNT_SID = settings['account_sid']
AUTH_TOKEN = settings['account_token']
TWILIO_SENDER_NUMBER = settings['twilio_sender_number']
TWILIO_NUMBERS = [ settings['tracker01'], settings['tracker02'] ]
def send_sms(dest='', source='', message='Python Test'):
	client = Client(ACCOUNT_SID, AUTH_TOKEN)
	new_message = client.messages.create(to=dest, from_=source, body=message)
	return new_message.sid

def main():
    for i in TWILIO_NUMBERS:
        message_id = send_sms(dest=i, source=TWILIO_SENDER_NUMBER, message='admin123456 +447491838747')
        print("Sending message " + message_id + " to: " + i)

if __name__ == "__main__":
	main()
