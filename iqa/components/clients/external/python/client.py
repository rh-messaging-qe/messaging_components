from autologging import logged, traced

from iqa.components.clients.external import ClientExternal, protocols
from iqa.system.node import Node, Executor


@logged
@traced
class ClientPython(ClientExternal):
    """Python Proton client (base abstract class)."""

    supported_protocols = [protocols.Amqp10()]
    implementation = 'python'
    version = '1.0.1'

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ClientPython, self).__init__(name, node, executor, **kwargs)
