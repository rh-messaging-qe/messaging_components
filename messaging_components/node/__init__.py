from messaging_components.node.node_docker import NodeDocker
from .node_local import *
from .node_ansible import *
from iqa_common.executor import *
from messaging_abstract.node.node import Node
import logging


class NodeFactory(object):

    logger = logging.getLogger(__name__)

    @staticmethod
    def create_node(hostname: str, executor: Executor, ip: str = None, **kwargs) -> Node:
        """
        Creates a Node object based on provided arguments.
        :param hostname:
        :param executor:
        :param ip:
        :param kwargs:
        :return:
        """

        if isinstance(executor, ExecutorAnsible):
            node = NodeAnsible(hostname, executor, ip)
        elif isinstance(executor, ExecutorContainer):
            node = NodeDocker(hostname, executor, ip)
        else:
            node = NodeLocal(hostname, executor, ip)

        NodeFactory.logger.info("Creating %s [hostname=%s, ip=%s]" % (node.__class__.__name__, hostname, ip))
        return node
