"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

import messaging_abstract.client
from .client import Client


@logged
@traced
class Connector(Client, messaging_abstract.client.Connector):
    """Core python connector client."""

    def __init__(self):
        messaging_abstract.client.Connector.__init__(self)
        Client.__init__(self)
