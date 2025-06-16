import os
from datetime import datetime, timedelta

import requests

from sheety_data import SheetyData

sheety_data = SheetyData()
sheety_data.get_and_update_iataCodes()  # update iata codes in the sheety rows

url = 'https://test.api.amadeus.com/v1/security/oauth2/token'


token_parameters = {
    'grant_type': 'client_credentials',
    'client_id': os.environ.get('flight_api_key'),
    'client_secret': os.environ.get('flight_api_secret'),
}
# token = requests.post(url=url, data=token_parameters)
# token.raise_for_status()
# print(token.json())

today = datetime.now()

tomorrow = today + timedelta(days=1)  # tomorrow's date

six_months_later = tomorrow + timedelta(days=6*30)  # Approximation of 6 months

# Generate a list of dates from tomorrow to six months later
date_list = [tomorrow + timedelta(days=i)
             for i in range((six_months_later - tomorrow).days + 1)]

for date in date_list:
    date.strftime('%Y-%m-%d')


class FlightSearch:
    def __init__(self, destination_code,):
        self.URL = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        self.origin_code = "KMS"  # Ksi airport code
        self.destination_code = destination_code
        self.from_date: list[datetime] = date_list
        self.header = {
            'authorization': f"Bearer {os.environ.get('flight_token')}",
        }

    def get_parameter_date(self, dateList: list[datetime]):
        """Convert a list of datetime objects to a list of strings in 'YYYY-MM-DD' format.

        """
        for date in dateList:
            if not isinstance(date, datetime):
                raise ValueError(
                    "All items in dateList must be datetime objects.")
            if not dateList:
                raise ValueError("dateList cannot be empty.")

            self.flight_search_parameters = {'originLocationCode': self.origin_code, 'destinationLocationCode': self.destination_code,
                                             'departureDate': date.strftime('%Y-%m-%d'), 'adults': 1, 'currencyCode': 'GHS', 'max': 5, }
            flight_response = requests.get(
                url=self.URL, headers=self.header, params=self.flight_search_parameters)
            flight_response.raise_for_status()
