import messaging_abstract.broker
from ..node import Node


class Broker(messaging_abstract.broker.Broker):
    """
    Broker component
    """
    def __init__(self, node: Node):
        self.node = node
