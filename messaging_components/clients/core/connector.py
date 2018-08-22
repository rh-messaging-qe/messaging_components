"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Connector, Node

from messaging_components.clients.core.client import ClientCore


@logged
@traced
class ConnectorCore(Connector, ClientCore):
    """Core python connector client."""
    def __init__(self, name: str, node: Node, executor: Executor):
        super(ConnectorCore, self).__init__(name, node, executor)
        #  TODO - Define what kind of object the core connector is going to use (maybe the default for python ext. client)
