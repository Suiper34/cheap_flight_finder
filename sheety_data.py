import os
from test import sheety_header

import requests


class SheetyData:
    def __init__(self):

        self.username = os.environ.get('sheety_username')

        self.sheety_url = f'https://api.sheety.co/{self.username}/cheapFlightDeals/prices'

        self.the_sheety_header = sheety_header

        self.sheety_response = requests.get(
            url=self.sheety_url, headers=self.the_sheety_header)
        self.sheety_response.raise_for_status()
        self.sheety_rows = self.sheety_response.json()
        print(self.sheety_rows)

    def get_and_update_iataCodes(self):
        """use the amadeus city search api to get iata codes for cities in the flights deal sheety rows and update the sheety rows with the iata codes."""
        # amadeus city search api
        city_url = 'https://test.api.amadeus.com/v1/reference-data/locations/cities'
        token = os.environ.get('flight_token')
        if not token:
            raise ValueError("Missing flight_token environment variable")
        header = {
            'authorization': f"Bearer {token}",
        }  # amadeus city authentication token

        for idx, i in enumerate(self.sheety_rows['prices']):
            city_parameter = {'keyword': (i['city'])}
            city_iatacodes_response = requests.get(
                url=city_url, params=city_parameter, headers=header)
            print(city_iatacodes_response.json())

            data = city_iatacodes_response.json().get('data', [])
            if not data:
                print(f"No IATA code found for {i['city']}")
                continue
            city_iatacodes = data[0]['iataCode']

            iatacodes_parameter = {'price': {'iataCode': city_iatacodes}}

            # using the actual row id
            sheety_put_request = f'{self.sheety_url}/{i["id"]}'
            iatacodes_put_response = requests.put(
                url=sheety_put_request, json=iatacodes_parameter, headers=self.the_sheety_header)
            iatacodes_put_response.raise_for_status()
            print(iatacodes_put_response.text)


sheety_data = SheetyData()
sheety_data.get_and_update_iataCodes()
