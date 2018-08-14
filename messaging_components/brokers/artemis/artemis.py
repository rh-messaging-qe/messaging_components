from ...brokers import Broker
from ...node import Node
from ...node.service import Service

import messaging_components.protocols as protocols


class ServiceArtemis(Service):
    def __init__(self, service, name, node: Node):
        super().__init__(node, name)
        self.service = service
        self.name = name

    def stop(self):
        """
        Service stop.
        :return: executed process
        """
        return self.service.node.ansible.cli_cmd(module='shell', host=self.service.node.hostname,
                                                 moduleargs=['killall java'])


class Artemis(Broker):
    """
    Apache ActiveMQ Artemis has a proven non blocking architecture. It delivers outstanding performance.
    """
    supported_protocols = [protocols.Amqp10(), protocols.Mqtt(), protocols.Stomp(), protocols.Openwire()]
    name = 'Artemis'

    def __init__(self, node: Node):
        Broker.__init__(self, node=node)
        self.service = ServiceArtemis(self, 'qdrouterd')


