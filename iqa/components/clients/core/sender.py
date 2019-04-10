"""
    # TODO jstejska: Package description
"""
from autologging import logged, traced

from iqa.components.clients.core.client import CoreMessagingClient
from iqa.messaging.abstract.client.sender import Sender
from iqa.system.node import Node, Executor


@logged
@traced
class SenderCore(Sender, CoreMessagingClient):
    """Core python sender client."""
    def __init__(self, name: str, node: Node, executor: Executor):
        super().__init__(name, node, executor)
        #  TODO - Define what kind of object the core sender is going to use (maybe the default for python ext. client)
