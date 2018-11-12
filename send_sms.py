import os
import yaml
import utils

from twilio.rest import Client


settings = utils.make_settings(os.environ.get('SETTINGS_FILE'))

ACCOUNT_SID = settings['account_sid']
AUTH_TOKEN = settings['account_token']
TWILIO_SENDER_NUMBER = settings['twilio_sender_number']
TWILIO_RECIPIENT_NUMBER = settings['tracker01']

def send_sms(dest='', source='', message='Python Test'):
	client = Client(ACCOUNT_SID, AUTH_TOKEN)
	new_message = client.messages.create(to=dest, from_=source, body=message)
	return new_message.sid

def main():
	print("Sending message.. " + send_sms(dest=TWILIO_RECIPIENT_NUMBER, source=TWILIO_SENDER_NUMBER, message='G123456#'))

if __name__ == "__main__":
	main()
