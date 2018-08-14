"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from .opt.brokerurl import BrokerURLPythonProton
from ..opt.msgproperty import MsgProperty
from ..opt.msgcontentlist import MsgContentList
from ..opt.msgcontentmap import MsgContentMap
from optconstruct.types.prefixed import Prefixed
from optconstruct.types import Toggle

import messaging_abstract.client
from .client import Client
from messaging_components.node.node import Node


@logged
@traced
class Sender(Client, messaging_abstract.client.Sender):
    """External Python-Proton sender client."""

    # client is installed from cli-rhea, node_app is there only for backward compability
    cli_command = ['cli-proton-python-sender']
    # Client-sender params for build execute command
    cli_params_transformation = [
        Toggle('help', '--help'),
        # Control options
        BrokerURLPythonProton('broker_url', '--broker-url'),
        Prefixed('count', '--count'),
        Prefixed('timeout', '--timeout'),
        Prefixed('close-sleep', '--close-sleep'),

        Prefixed('sync-mode', '--sync-mode'),
        Prefixed('duration', '--duration'),
        Prefixed('duration-mode', '--duration-mode'),
        Prefixed('capacity', '--capacity'),

        # Logging options
        Prefixed('log-lib', '--log-lib'),
        Prefixed('log-stats', '--log-stats'),
        Prefixed('log-msgs', '--log-msgs'),

        # Transaction options
        Prefixed('tx-size', '--tx-size'),
        Prefixed('tx-action', '--tx-action'),
        Prefixed('tx-endloop-action', '--tx-endloop-action'),

        # Connection options
        Prefixed('conn-urls', '--conn-urls'),
        Prefixed('conn-reconnect', '--conn-reconnect'),
        Prefixed('conn-reconnect_interval', '--conn-reconnect-interval'),
        Prefixed('conn-reconnect_limit', '--conn-reconnect-limit'),
        Prefixed('conn-reconnect_timeout', '--conn-reconnect-timeout'),
        Prefixed('conn-heartbeat', '--conn-heartbeat'),
        Prefixed('conn-ssl-certificate', '--conn-ssl-certificate'),
        Prefixed('conn-ssl-private_key', '--conn-ssl-private-key'),
        Prefixed('conn-ssl-password', '--conn-ssl-password'),
        Prefixed('conn-ssl-trust-store', '--conn-ssl-trust-store'),
        Toggle('conn-ssl-verify-peer', '--conn-ssl-verify-peer'),
        Toggle('conn-ssl-verify-peer-name', '--conn-ssl-verify-peer-name'),
        Prefixed('conn-handler', '--conn-handler'),
        Prefixed('conn-max-frame-size', '--conn-max-frame-size'),

        # Link options
        Toggle('link-durable', '--link-durable'),
        Toggle('link-at-least-once', '--link-at-least-once'),
        Toggle('link-at-most-once', '--link-at-most-once'),

        # Message options
        Prefixed('msg-id', '--msg-id'),
        Prefixed('msg-subject', '--msg-subject'),
        Prefixed('msg-reply-to', '--msg-reply-to'),
        Prefixed('msg-durable', '--msg-durable'),
        Prefixed('msg-ttl', '--msg-ttl'),
        Prefixed('msg-priority', '--msg-priority'),
        Prefixed('msg-correlation-id', '--msg-correlation-id'),
        Prefixed('msg-user-id', '--msg-user-id'),
        Prefixed('msg-group-id', '--msg-group-id'),
        MsgProperty('msg-property', '--msg-property'),
        MsgContentMap('msg-content-map-item', '--msg-content-map-item'),
        MsgContentList('msg-content-list-item', '--msg-content-list-item'),
        Prefixed('msg-content-from-file', '--msg-content-from-file'),
        Prefixed('msg-content', '--msg-content'),
        Prefixed('msg-content-type', '--msg-content-type'),
        Prefixed('content-type', '--content-type'),

        # Reactor options
        Toggle('reactor-peer-close-is-error', '--reactor-peer-close-is-error'),
        Toggle('reactor-auto-settle-off', '--reactor-auto-settle-off'),

    ]

    def __init__(self, node: Node):
        """Init of Python sender."""

        messaging_abstract.client.Sender.__init__(self)
        Client.__init__(self, node)

    def _send_message(self, **kwargs):
        """Send message.

        :param kwargs: # TODO jstejska: Description
        :type kwargs:
        :return:
        :rtype:
        """
        self._set_attr_values(kwargs)
        cmd = self._build_sender_command()
        self._execute(cmd)
