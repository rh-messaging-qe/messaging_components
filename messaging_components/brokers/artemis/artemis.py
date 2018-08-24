from iqa_common.executor import Executor
from messaging_abstract.component.server.broker import Broker
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node

import messaging_components.protocols as protocols


class Artemis(Broker):
    """
    Apache ActiveMQ Artemis has a proven non blocking architecture. It delivers outstanding performance.
    """
    supported_protocols = [protocols.Amqp10(), protocols.Mqtt(), protocols.Stomp(), protocols.Openwire()]
    name = 'Artemis'
    implementation = 'artemis'

    def __init__(self, name: str, node: Node, executor: Executor, service: Service,
                 broker_name: str=None, config: str=None, web_port=8161, **kwargs):
        super(Artemis, self).__init__(name, node, executor, service, broker_name,
                                      config, web_port, **kwargs)
