from autologging import logged, traced
from messaging_abstract.protocol.protocol import Protocol
from messaging_components.network.transport import TCP


@logged
@traced
class Openwire(Protocol):
    def __init__(self, transport=TCP, default_port=5672):
        super(Openwire, self).__init__(transport, default_port)
