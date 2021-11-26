import africastalking

# TODO: Initialize Africa's Talking

africastalking.initialize(
    username='sandbox',
    api_key=''
)


class SendSMS():
    sms = africastalking.SMS

    def send(self):

        # TODO: Send message

        recipients = ["+265995160682"]
        # Set your message
        message = "Hey AT this is a test message"
        # Set your shortCode or senderId

        try:
            response = self.sms.send(message, recipients)
            print(response)
        except Exception as e:
            print(f'Houston, we have a problem: {e}')