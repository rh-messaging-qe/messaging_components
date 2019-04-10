from iqa.components.abstract.server.server_component import ServerComponent
from iqa.messaging.abstract.server.broker import Broker
from iqa.components import protocols


class Qpid(Broker, ServerComponent):
    """
    Qpid broker
    A message-oriented middleware message broker written in C++ that stores, routes, and forwards messages using AMQP.
    """
    supported_protocols = [protocols.Amqp10()]
    name = 'Qpid C++ Broker'
    implementation = 'qpid'

    def __init__(self, name: str, **kwargs):
        super(Qpid, self).__init__(name, **kwargs)
