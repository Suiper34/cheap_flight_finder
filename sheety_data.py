import os
from test import sheety_header

import requests


class SheetyData:
    def __init__(self):

        self.username = os.environ.get('username')

        self.sheety_url = f'https://api.sheety.co/{self.username}/cheapFlightDeals/prices'

        the_sheety_header = sheety_header

        self.sheety_parameters = {}

        self.sheety_response = requests.get(
            url=self.sheety_url, headers=the_sheety_header)
        self.sheety_response.raise_for_status()
        self.sheety_rows = self.sheety_response.json()
        print(self.sheety_rows)


SheetyData()
