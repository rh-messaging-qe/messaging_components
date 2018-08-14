"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from messaging_abstract.client import Client
from messaging_abstract.broker import Broker
from messaging_abstract.router import Router

from .executions import AnsibleCMD, AnsibleExecution
from .executions import Executor


@logged
@traced
class Node:
    """Node component."""

    def __init__(self, hostname, ansible: AnsibleCMD, ip=None, execution=None):
        self.hostname = hostname
        Node.__log.info('Initialization of node %s..' % self.hostname)
        self.ansible = AnsibleExecution(hostname, ansible_cmd=ansible)
        self.executor = Executor(hostname)

        # Execution, by default is used Ansible
        if 'Executor' == execution:
            self.execution = self.executor
        else:
            self.execution = self.ansible

        self.ip = ip if ip else self._get_ip()
        self.components = []

    def execute(self, command):
        """Execute command on node"""
        return self.execution.execute(command)

    def ping(self):
        """Send ping to node"""
        return self.ansible.ping()

    def _get_ip(self):
        """Get ip of node"""
        cmd_ip = 'ip route | grep ^default | grep -oE [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'
        process = self.execute(cmd_ip)
        return process.get_stdout()

    def new_component(self, component):
        """Adding component to under node.

        :param component:
        :type component:

        :return: Component object
        :rtype:
        """
        component = component(node=self)
        self.components.append(component)
        return component
    
    @property
    def brokers(self):
        """
        Get all broker instances on this node
        :return:
        """
        return [component for component in self.components
                if issubclass(component, Broker)]

    @property
    def clients(self):
        """
        Get all client instances on this node
        @TODO
        :return:
        """
        return [component for component in self.components
                if issubclass(component, Client)]

    @property
    def routers(self):
        """
        Get all router instances on this node
        @TODO
        :return:
        """
        return [component for component in self.components
                if issubclass(component, Router)]
