import os
from test import sheety_header

import requests


class GetUsersEmails:
    """Get user emails from Sheety API."""

    def __init__(self):
        self.username = os.environ.get('sheety_username')
        if not self.username:
            raise ValueError('Missing sheety username')

        self.user_mail_url = f'https://api.sheety.co/{self.username}/cheapFlightDeals/users'
        self.header = sheety_header
        self.fetch_user_emails()

    def fetch_user_emails(self) -> list:
        """Fetch user emails from Sheety API."""
        try:
            email_response = requests.get(
                url=self.user_mail_url, headers=self.header)
            email_response.raise_for_status()
            return email_response.json().get('users', [])
        except Exception as e:
            print(f'Failed to fetch user emails: {e}')
            return []

    def user_emails_list(self) -> list:
        """Extract emails from the response into a list."""
        emails_data = self.fetch_user_emails()
        if not emails_data:
            raise ValueError('No user data found in the response.')
        if not isinstance(emails_data, list):
            raise ValueError(
                'Expected "users" to be a list in the response data.')
        users_emails = [a_dict['email'] for a_dict in emails_data]
        return users_emails
