"""
Ansible Node implementation of Node Interface.
"""

from iqa_common.executor import Executor
import logging

from iqa_common.utils.docker_util import DockerUtil
from messaging_abstract.node.node import Node


class NodeDocker(Node):
    """Ansible implementation for Node interface."""

    def __init__(self, hostname: str, executor: Executor, ip: str=None):
        super(NodeDocker, self).__init__(hostname, executor, ip)
        self.docker_util = DockerUtil()
        self.ip = ip
        logging.getLogger().info('Initialization of NodeDocker: %s' % self.hostname)

    def ping(self) -> bool:
        """Send ping to Docker node"""
        try:
            container = DockerUtil().get_container(self.executor.container_name)
            return container.attrs['State']['Running']
        except:
            logging.info("Unable to get container status for: %s" % self.executor.container_name)
            return False

    def get_ip(self) -> str:
        """Get ip of Docker node"""
        if self.ip is not None:
            return self.ip

        try:
            docker_network = self.executor.docker_network or 'bridge'
            logging.debug("Retrieving container's ip for network: %s" % docker_network)
            ip = self.docker_util.get_container_ip(self.executor.container_name,
                                                   docker_network)
        except:
            logging.debug("Unable to determine IP for container: %s" % self.executor.container_name)
            return None

        logging.debug("Container [%s] - IP [%s]" % (self.executor.container_name, ip))
        self.ip = ip
        return ip
