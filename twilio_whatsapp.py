import os
import smtplib
from email.message import EmailMessage

from twilio.rest import Client

from get_users_emails import GetUsersEmails

# instantiating user emails class
get_users_emails = GetUsersEmails()


class TwilioWhatsApp:
    """send WhatsApp messages using Twilio."""

    def __init__(self,):
        """Initialize Twilio WhatsApp client."""
        self.account_sid = os.environ.get('whatsapp_account_sid')
        self.auth_token = os.environ.get('whatsapp_auth_token')
        if not self.account_sid or not self.auth_token:
            raise ValueError(
                "Missing Twilio account SID or auth token environment variable")
        self.client = Client(self.account_sid, self.auth_token)

    def send_whatsapp_message(self, body: str,):
        """send the cheapest flight deals via whatsapp."""
        if not body:
            raise ValueError("Message body cannot be empty")
        if not isinstance(body, str):
            raise TypeError("Message body must be a string")
        try:
            message = self.client.messages.create(
                from_=os.environ.get('whatsapp_sender'),
                body=body,
                to='whatsapp:+233544078214',
            )
            print(message.sid)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")


class SendEmail:
    def __init__(self,):
        self.username = os.environ.get('email_username')
        self.password = os.environ.get('email_password')
        self.receivers = get_users_emails.user_emails_list()

    def send_email(self, body: str,):
        """send message via email"""
        receivers = self.receivers.copy()
        extra_receiver = os.environ.get('receiver')
        # append extra receiver if it exists
        receivers.append(extra_receiver) if extra_receiver else None
        with smtplib.SMTP_SSL('smtp.gmail.com') as send_mail:
            send_mail.login(user=self.username, password=self.password)

            msg = EmailMessage()
            msg.set_content(body)
            msg['From'] = self.username
            msg['Subject'] = 'Found A Cheap Flight Deal'
            msg['To'] = ', '.join(receivers)

            send_mail.send_message(msg)
