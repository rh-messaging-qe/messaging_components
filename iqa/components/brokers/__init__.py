from messaging_abstract.component import *
from messaging_abstract.node.node import Node

from .artemis import Artemis
from .qpid import Qpid


class BrokerFactory(object):

    @staticmethod
    def create_broker(implementation: str, node: Node, executor: Executor, service_impl: Service, **kwargs):

        for broker in Broker.__subclasses__():

            # Ignore broker with different implementation
            if broker.implementation != implementation:
                continue

            name = '%s-%s-%s' % ('broker', broker.__name__, node.hostname)
            return broker(name=name, node=node, executor=executor, service=service_impl, **kwargs)

        raise ValueError('Invalid broker implementation: %s' % implementation)
