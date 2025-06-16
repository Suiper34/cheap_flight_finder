import os

import requests

from sheety_data import SheetyData

# sheety_data = SheetyData()
# sheety_data.get_and_update_iataCodes() #update iata codes in the sheety rows

URL = 'https://test.api.amadeus.com/v2/shopping/flight-offers'

url = 'https://test.api.amadeus.com/v1/security/oauth2/token'


token_parameters = {
    'grant_type': 'client_credentials',
    'client_id': os.environ.get('flight_api_key'),
    'client_secret': os.environ.get('flight_api_secret'),
}
token = requests.post(url=url, data=token_parameters)
token.raise_for_status()
print(token.json())
