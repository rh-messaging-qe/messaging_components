"""
    # TODO jstejska: Package description
"""
from autologging import logged, traced

from iqa.messaging.abstract.client.sender import Sender


@logged
@traced
class SenderCore(Sender, ClientCore):
    """Core python sender client."""
    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderCore, self).__init__(name, node, executor)
        #  TODO - Define what kind of object the core sender is going to use (maybe the default for python ext. client)
