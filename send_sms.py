import os
import yaml

from twilio.rest import Client


def make_settings(settingsfile_path):
    with open(settingsfile_path, 'r') as settingsfile:
        return yaml.load(settingsfile)

settings = make_settings(os.environ.get('SETTINGS_FILE'))

ACCOUNT_SID = settings['account_sid']
AUTH_TOKEN = settings['account_token']
TWILIO_SENDER_NUMBER = settings['twilio_sender_number']

def send_sms(dest='', source='', message='Python Test'):
	client = Client(ACCOUNT_SID, AUTH_TOKEN)
	new_message = client.messages.create(to=dest, from_=source, body=message)
	return new_message.sid

def main():
	print("Sending message.. " + send_sms(dest='+447491838747', source=TWILIO_SENDER_NUMBER))

if __name__ == "__main__":
	main()
