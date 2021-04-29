from sendsms.backends.base import BaseSmsBackend
import some.sms.delivery.api

class AwesomeSmsBackend(BaseSmsBackend):
    def send_messages(self, messages):
        for message in messages:
            for to in message.to:
                try:
                    some.sms.delivery.api.send(
                        message=message.body,
                        from_phone=message.from_phone,
                        to_phone=to,
                        flashing=message.flash
                    )
                except:
                    if not self.fail_silently:
                        raise