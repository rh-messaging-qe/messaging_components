from autologging import logged, traced

from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


@logged
@traced
class Amqp(Protocol):
    def __init__(self, transport=TCP, default_port=5672):
        super(Amqp, self).__init__(transport, default_port)
        self.name = "AMQP"


class Amqp10(Amqp):
    def __init__(self, transport=TCP, default_port=5672):
        super(Amqp10, self).__init__(transport, default_port)
        self.name = "AMQP 1.0"


class Amqp091(Amqp):
    def __init__(self, transport=TCP, default_port=5672):
        super(Amqp091, self).__init__(transport, default_port)
        self.name = "AMQP 0.9.1"
