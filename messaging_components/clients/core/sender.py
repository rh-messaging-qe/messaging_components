"""
    # TODO jstejska: Package description
"""
from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Sender, Node

from messaging_components.clients.core.client import ClientCore


@logged
@traced
class SenderCore(Sender, ClientCore):
    """Core python sender client."""
    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderCore, self).__init__(name, node, executor)
        #  TODO - Define what kind of object the core sender is going to use (maybe the default for python ext. client)
