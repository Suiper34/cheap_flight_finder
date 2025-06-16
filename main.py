import os
from test import sheety_header

import requests

from flight_search import FlightSearch
from sheety_data import SheetyData
from twilio_whatsapp import SendEmail, TwilioWhatsApp

sheety_data = SheetyData()
sheety_data.get_and_update_iataCodes()  # update iata codes in the sheety rows

#
username = os.environ.get('sheety_username')
sheety_url = f'https://api.sheety.co/{username}/cheapFlightDeals/prices'
the_sheety_header = sheety_header
sheety_response = requests.get(
    url=sheety_url, headers=the_sheety_header)
sheety_response.raise_for_status()
flight_deal_data = sheety_response.json()['prices']

for i in flight_deal_data:
    flight_search = FlightSearch(
        flight_deal_data[i]['iataCode'], flight_deal_data[i]['lowestPrice'])
