"""
    # TODO jstejska: Package description
"""
from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Receiver, Node

from messaging_components.clients.core.client import ClientCore


@logged
@traced
class ReceiverCore(Receiver, ClientCore):
    """Core python receiver client."""
    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverCore, self).__init__(name, node, executor)
        #  TODO - Define what kind of object the core receiver is going to use (maybe the default for python ext. client)
