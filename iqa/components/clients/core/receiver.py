"""
    # TODO jstejska: Package description
"""
from autologging import logged, traced
from iqa.components.clients.core.client import CoreMessagingClient
from iqa.messaging.abstract.client.receiver import Receiver
from iqa.system.node import Node, Executor


@logged
@traced
class ReceiverCore(Receiver, CoreMessagingClient):
    """Core python receiver client."""
    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverCore, self).__init__(name, node, executor)
        #  TODO - Define what kind of object the core receiver is going to use (maybe the default for python ext. client)
