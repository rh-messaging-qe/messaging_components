import messaging_abstract.router
from ..node import Node


class Router(messaging_abstract.router.Router):
    """
    Router component
    """
    def __init__(self, node: Node):
        self.node = node
