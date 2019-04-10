from autologging import logged, traced
from iqa.components.abstract.network.protocol import Protocol
from iqa.components.abstract.network.transport import TCP


@logged
@traced
class Openwire(Protocol):
    def __init__(self, transport=TCP, default_port=5672):
        super(Openwire, self).__init__(transport, default_port)
