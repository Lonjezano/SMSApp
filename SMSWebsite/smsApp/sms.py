import africastalking
from django.contrib.auth.mixins import LoginRequiredMixin
from .views import SMS

# TODO: Initialize Africa's Talking

africastalking.initialize(
    username='sandbox',
    api_key=''
)


class SendSMS():
    sms = africastalking.SMS
    phone_number = None
    message = None

    def send(self):
        # TODO: Send message

        recipients = self.phone_number
        # Set your message
        message = str(self.message)
        # Set your shortCode or senderId

        try:
            return self.sms.send(message, recipients)

        except Exception as e:
            return e
