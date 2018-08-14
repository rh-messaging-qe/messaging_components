"""
    Package for testing nodejs external client sender.
"""

import unittest
import mock
from messaging_components.clients.external.nodejs import Sender


class NodejsExternalSender(unittest.TestCase):
    """Sender command builder test class."""

    @classmethod
    @mock.patch('messaging_components.node.Node')
    def setup_class(cls, mock_cls):
        """Class setup."""

        cls.sender = Sender(mock_cls)

    def test_name(self):
        """Check if created sender is available in the test-suite.

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
        prefix = 'cli-rhea-sender'
        assert self.sender.cli_command[0] == prefix

    def test_minimal_message_command_build(self):
        """Test for minimal message command build based on specified data structure.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'msg-content': 'test-msg',
            'count': '5',
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[0] + ' --msg-content test-msg --broker 10.0.0.1:5672 --address queue --count 5'

        assert str_cmd == command

    def test_link_durable_message_command_build(self):
        """Test for durable message command build based on specified data structure.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'msg-content': 'test-msg',
            'count': '5',
            'link-durable': True,
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[
                      0] + ' --msg-content test-msg --broker 10.0.0.1:5672 --address queue --count 5 --link-durable'

        assert str_cmd == command

    def test_msg_property_build(self):
        """Test for msg_property option build.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'msg-content': 'test-msg',
            'count': '5',
            'msg-property': {
                '~': {
                    'key1': 'val1'
                },
                '=': {
                    'key2': 'val2'
                },
                'key3': 'val3'
            },
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[
                      0] + ' --msg-property \"key1~val1\" --msg-property \"key2=val2\" --msg-property \"key3=val3\"  ' \
                           '--msg-content test-msg --broker 10.0.0.1:5672 --address queue --count 5'

        assert str_cmd == command

    def test_msg_content_list_build(self):
        """Test for msg_property option build.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'msg-content': 'test-msg',
            'count': '5',
            'msg-content-list-item': (10, 5),
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[
                      0] + ' --msg-content-list-item \"~10\" --msg-content-list-item \"~5\"  ' \
                           '--msg-content test-msg --broker 10.0.0.1:5672 --address queue --count 5'

        assert str_cmd == command

    def test_msg_content_map_build(self):
        """Test for msg_property option build.

        :return:
        :rtype:
        """
        self.sender.data = {
            'host': '10.0.0.1',
            'port': '5672',
            'address': 'queue',
            'msg-content': 'test-msg',
            'count': '5',
            'msg-content-map-item': {
                '~': {
                    'key1': 'val1'
                },
                '=': {
                    'key2': 'val2'
                },
                'key3': 'val3'
            }
        }
        str_cmd, _ = self.sender.build_command()

        command = self.sender.cli_command[
                      0] + ' --msg-content-map-item \"key1~val1\" --msg-content-map-item \"key2=val2\" ' \
                           '--msg-content-map-item \"key3=val3\"  --msg-content test-msg ' \
                           '--broker 10.0.0.1:5672 --address queue --count 5'

        assert str_cmd == command
