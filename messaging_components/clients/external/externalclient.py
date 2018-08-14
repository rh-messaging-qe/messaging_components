"""
    # TODO jstejska: Package description
"""

from messaging_abstract.client.client import Client
from messaging_components.node import Node


class ExternalClient(Client):
    """External CLI based clients."""

    # attribute-argument mapping dictionary
    cli_params_transformation = []
    cli_command = []
    data = set()

    def __init__(self, node: Node):
        super(ExternalClient, self).__init__()
        self.node = node

    @staticmethod
    def _run():
        """ # TODO jstejska: Description

        :return: # TODO jstejska: Description
        :rtype: # TODO jstejska: type
        """
        assert NotImplementedError

    def _execute(self, cmd):
        """Method for execute client's command.

        :param cmd: command
        :type cmd: # TODO jstejska: type

        :return: # TODO jstejska: Description
        :rtype: # TODO jstejska: type
        """
        self.node.execute(cmd)

    def build_command(self):
        """Method for create command for execute based on client's available attributes.

        :return: list with command attributes
        :rtype: # TODO jstejska: type
        """

        cmd = [
            opt.generate(self.data)
            for opt in self.cli_params_transformation
            if opt.satisfied(self.data)
        ]

        cmd = self.cli_command + cmd

        return " ".join(filter(None, cmd)), cmd
