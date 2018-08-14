"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

import messaging_abstract.client
from .client import Client


@logged
@traced
class Receiver(Client, messaging_abstract.client.Receiver):
    """Core python receiver client."""

    def __init__(self):
        messaging_abstract.client.Receiver.__init__(self)
        Client.__init__(self)
