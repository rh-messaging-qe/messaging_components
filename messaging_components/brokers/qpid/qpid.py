from iqa_common.executor import Executor
from messaging_abstract.component.server.broker import Broker
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node

import messaging_components.protocols as protocols


class Qpid(Broker):
    """
    Qpid broker
    A message-oriented middleware message broker written in C++ that stores, routes, and forwards messages using AMQP.
    """
    supported_protocols = [protocols.Amqp10()]
    name = 'Qpid C++ Broker'
    implementation = 'qpid'

    def __init__(self, name: str, node: Node, executor: Executor, service: Service,
                 broker_name: str=None, config: str=None, web_port=8161, **kwargs):
        super(Qpid, self).__init__(name, node, executor, service, broker_name,
                                   config, web_port, **kwargs)
