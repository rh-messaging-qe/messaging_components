import iqa
from iqa.messaging.abstract.message import Message


class Message(Message):
    """
    AMQP10 Message
    """
    def __init__(self):
        iqa.messaging_abstract.message.Message.__init__(self)
