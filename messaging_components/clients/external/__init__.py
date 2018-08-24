from messaging_abstract.component import *
from .nodejs import *
from .python import *
from .java import *


class ClientFactory(object):

    @staticmethod
    def create_clients(implementation: str, node: Node, executor: Executor) -> list:

        for client in ClientExternal.__subclasses__():

            # Ignore clients with different implementation
            if client.implementation != implementation:
                continue

            # Now loop through concrete client types (sender, receiver, connector)
            clients = []
            for client_impl in client.__subclasses__():
                name = '%s-%s-%s' % (implementation, client_impl.__name__.lower(), node.hostname)
                clients.append(client_impl(name=name, node=node, executor=executor))

            return clients

        raise ValueError('Invalid client implementation')
