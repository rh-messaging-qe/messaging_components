"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from messaging_components.node import Node

import messaging_components.protocols as protocols
from messaging_components.clients.external.externalclient import ExternalClient


@logged
@traced
class Client(ExternalClient):
    """Python Proton client."""

    supported_protocols = [protocols.Amqp10()]
    name = 'Python Proton client'
    version = '1.0.1'

    def __init__(self, node: Node):
        ExternalClient.__init__(self, node)

