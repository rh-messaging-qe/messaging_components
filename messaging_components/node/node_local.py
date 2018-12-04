"""
Basic concrete implementation of Node interface.
"""

from iqa_common.executor import Executor, Command, Execution, ExecutorAnsible, CommandAnsible
import re
import logging

from messaging_abstract.node.node import Node


class NodeLocal(Node):
    """Node component."""

    def __init__(self, hostname: str, executor: Executor, ip: str=None):
        super(NodeLocal, self).__init__(hostname, executor, ip)
        logging.getLogger().info('Initialization of NodeLocal: %s' % self.hostname)

    def ping(self) -> bool:
        """Send ping to node"""
        cmd_ping = Command([], stdout=True, timeout=20)

        # If unable to determine ip address, then do not perform ping
        if self._get_ip() is None:
            return False
        cmd_ping.args = ['ping', '-c', '1', self._get_ip()]

        execution = self.executor.execute(cmd_ping)

        # True if completed with exit code 0 and stdout has some data
        return execution.completed_successfully() and bool(execution.read_stdout())

    def get_ip(self):
        """Get ip of node"""
        if self.ip is not None:
            return self.ip

        cmd_ip = Command(['ip', 'addr', 'list'], stdout=True, timeout=10)
        execution = self.execute(cmd_ip)

        # If execution failed, skip it
        if not execution.completed_successfully():
            return None

        # Parsing stdout and retrieving the IP
        ip_addr_out = execution.read_stdout()
        if not ip_addr_out:
            return None

        # Parse all returned ip addresses
        ip_addresses = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', ip_addr_out, re.MULTILINE)
        try:
            ip_addresses.remove('127.0.0.1')
        except ValueError:
            return None

        # If only loop back defined, skip it
        if not ip_addresses:
            return None

        return ip_addresses[0]
