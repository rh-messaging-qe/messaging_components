from autologging import logged, traced

from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


@logged
@traced
class Stomp(Protocol):
    def __init__(self, transport=TCP, default_port=5672):
        super(Stomp, self).__init__(transport, default_port)