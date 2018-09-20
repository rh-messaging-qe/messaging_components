"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from messaging_abstract.component.client import Node, Executor
import messaging_components.protocols as protocols
from messaging_components.clients.external import ClientExternal


@logged
@traced
class ClientNodeJS(ClientExternal):
    """NodeJS RHEA client"""

    supported_protocols = [protocols.Amqp10()]
    implementation = 'nodejs'
    version = '1.0.1'

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ClientNodeJS, self).__init__(name, node, executor, **kwargs)
