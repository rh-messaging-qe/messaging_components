from messaging_abstract.component import *
from .dispatch import *


class RouterFactory(object):

    @staticmethod
    def create_router(implementation: str, node: Node, executor: Executor, service_impl: Service, **kwargs):

        for router in Router.__subclasses__():

            # Ignore router with different implementation
            if router.implementation != implementation:
                continue

            name = '%s-%s-%s' % ('router', router.__name__, node.hostname)
            return router(name=name, node=node, executor=executor, service=service_impl, **kwargs)

        raise ValueError('Invalid router implementation: %s' % implementation)
