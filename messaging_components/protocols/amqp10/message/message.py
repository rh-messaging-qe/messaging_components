import messaging_abstract.message


class Message(messaging_abstract.message.Message):
    """
    AMQP10 Message
    """
    def __init__(self):
        messaging_abstract.message.Message.__init__(self)
