"""
    Package for testing nodejs external client receiver.
"""

import unittest
import mock
from messaging_components.clients.external.nodejs import Receiver


class NodejsExternalSender(unittest.TestCase):
    """Receiver command builder test class."""

    @classmethod
    @mock.patch('messaging_components.node.Node')
    def setup_class(cls, mock_cls):
        """Class setup."""

        cls.sender = Receiver(mock_cls)

    def test_name(self):
        """Check if created receiver is available in the test-suite.

        :return:
        :rtype:
        """
        name = 'NodeJS RHEA client'
        assert self.sender.name == name

    def test_command_prefix(self):
        """

        :return:
        :rtype:
        """
        prefix = 'cli-rhea-receiver'
        assert self.sender.cli_command[0] == prefix

    def test_minimal_message_command_build(self):
        """Test for minimal message receive command build based on specified data structure.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'count': '5',
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[0] + ' --broker 10.0.0.1:5672 --address queue --count 5'

        assert str_cmd == command

    def test_link_durable_message_command_build(self):
        """Test for durable message receive command build based on specified data structure.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'count': '5',
            'link-durable': True,
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[
                      0] + ' --broker 10.0.0.1:5672 --address queue --count 5 --link-durable'

        assert str_cmd == command
