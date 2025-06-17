import os
from datetime import datetime, timedelta

import requests

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


class FlightSearch:
    def __init__(self, destination_code, preferred_price: float):
        self.URL = 'https://test.api.amadeus.com/v2/shopping/flight-offers'
        self.origin_code = "KMS"  # Ksi airport code
        self.destination_code = destination_code
        self.from_date: list[datetime] = date_list
        self.header = {
            'authorization': f"Bearer {os.environ.get('flight_token')}",
        }
        self.preferred_price = preferred_price
        self.flight_search_parameters: dict = {}
        self.flight_offers_data: list = []
        self.message: str = ''
        self.get_parameter_date()

    def get_parameter_date(self,):
        """Convert a list of datetime objects to a list of strings in 'YYYY-MM-DD' format.
            Gets flight offers data for a list of dates.
        """
        for date in self.from_date:
            if not isinstance(date, datetime):
                raise ValueError(
                    "All items in self.from_date must be datetime objects.")
            if not self.from_date:
                raise ValueError("self.from_date cannot be empty.")

            self.flight_search_parameters = {'originLocationCode': self.origin_code, 'destinationLocationCode': self.destination_code,
                                             'departureDate': date.strftime('%Y-%m-%d'), 'adults': 1, 'currencyCode': 'GHS', 'max': 5, }
            try:
                flight_response = requests.get(
                    url=self.URL, headers=self.header, params=self.flight_search_parameters, timeout=15)
                flight_response.raise_for_status()
                data = flight_response.json().get('data', [])
            except Exception as e:
                print(f"Error fetching flights for {date}: {e}")
                continue
            self.flight_offers_data = data
            if not self.flight_offers_data:
                continue

            # check if flight offer price meet or is less than preferred price
            for flight_dict in self.flight_offers_data:
                try:
                    price = float(flight_dict['price']['total'])
                except (KeyError, ValueError, TypeError):
                    continue
                if price <= self.preferred_price:
                    try:
                        flight_date = flight_dict['itineraries'][0]['segments'][0]['departure']['at'].split('T')[
                            0]
                    except (KeyError, IndexError):
                        flight_date = 'Unknown date'
                    self.message += f"On {flight_date},\nthere is flight moving from Kumasi to {self.destination_code}\nat a price of GHS {flight_dict['price']['total']}\nwhich meet the preferred price requirement.\n"
                    return self.message
