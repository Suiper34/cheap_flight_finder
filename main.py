import os
from test import sheety_header

import requests

from flight_search import FlightSearch
from sheety_data import SheetyData
from twilio_whatsapp import SendEmail, TwilioWhatsApp

MAX_MESSAGES = 10
# the max length of Twilio WhatsApp message is 1600 characters
MAX_TWILIO_MESSAGE_LENGTH = 1600
sent_count = 0

sheety_data = SheetyData()
sheety_data.get_and_update_iataCodes()  # update iata codes in the sheety rows

# get updated flight deal sheet with iata codes
username = os.environ.get('sheety_username')
if not username:
    raise ValueError("Missing sheety_username environment variable")
sheety_url = f'https://api.sheety.co/{username}/cheapFlightDeals/prices'
the_sheety_header = sheety_header
sheety_response = requests.get(
    url=sheety_url, headers=the_sheety_header)
sheety_response.raise_for_status()
flight_deal_data = sheety_response.json()['prices']


for flight_offer in flight_deal_data:
    iata_code = flight_offer['iataCode']
    lowest_price = flight_offer['lowestPrice']
    if not iata_code or not lowest_price:
        print(f'Skipping flight offer {flight_offer} due to missing data.')
        continue
    flight_search = FlightSearch(
        iata_code, lowest_price)

    if not flight_search.message:
        print(f'No message generated for {iata_code}')
        continue

    # allow not more than 10 messages to be sent
    if flight_search.message:
        if sent_count >= MAX_MESSAGES:
            print("Reached message sending limit.")
            break

        # check if message length exceeds Twilio's limit then truncate it
        if len(flight_search.message) > MAX_TWILIO_MESSAGE_LENGTH:
            print("Message too long for Twilio, truncating.")
            flight_search.message = flight_search.message[:
                                                          MAX_TWILIO_MESSAGE_LENGTH - 3] + "..."

        twilio_whatsapp = TwilioWhatsApp()
        try:
            twilio_whatsapp.send_whatsapp_message(flight_search.message)
            sent_count += 1
        except Exception as e:
            print(f'Failed to send WhatsApp message: {e}')

    # send via message email
    send_mail = SendEmail()
    try:
        send_mail.send_email(flight_search.message)
    except Exception as e:
        print(f'Failed to send email: {e}')
