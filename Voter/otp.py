from django.conf import settings
from twilio.rest import Client


class OtpHandler:
    phone_number=None

    def __init__(self, phone_number) -> None:
        self.phone_number=phone_number

    def send_otp(self):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        verification = client.verify.v2.services(settings.TWILIO_VERIFY_SID) \
            .verifications \
            .create(to='+91'+str(self.phone_number), channel="sms")


