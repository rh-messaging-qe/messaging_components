"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from iqa.components import protocols
from iqa.components.clients.external import ClientExternal
from iqa.system.node import Node, Executor


@logged
@traced
class ClientNodeJS(ClientExternal):
    """NodeJS RHEA client"""

    supported_protocols = [protocols.Amqp10()]
    implementation = 'nodejs'
    version = '1.0.1'

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ClientNodeJS, self).__init__(name, node, executor, **kwargs)
