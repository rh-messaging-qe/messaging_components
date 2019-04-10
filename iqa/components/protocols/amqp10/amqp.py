from iqa.components.abstract.network.protocol import Protocol
from iqa.messaging.abstract.message import Message


class AMQP10(Protocol):
    """
    AMQP 1.0 Protocol implementation
    """
    def __init__(self):
        Protocol.__init__(
            self,
            message=Message(),
            transaction=NotImplementedError,
            transport=NotImplementedError,
            default_port=NotImplementedError
        )
    pass
