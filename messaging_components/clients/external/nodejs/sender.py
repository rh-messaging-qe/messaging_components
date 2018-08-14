"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from .opt.brokerurl import BrokerURLnodeJS
from ..opt.msgproperty import MsgProperty
from ..opt.msgcontentlist import MsgContentList
from ..opt.msgcontentmap import MsgContentMap
from optconstruct.types.prefixed import Prefixed
from optconstruct.types import Toggle

import messaging_abstract.client
from messaging_components.node.node import Node
from .client import Client


@logged
@traced
class Sender(Client, messaging_abstract.client.Sender):
    """External NodeJS sender client."""
    # client is installed from cli-rhea, node_app is there only for backward compatibility
    cli_command = ['cli-rhea-sender']

    # Client-receiver params for build execute command
    cli_params_transformation = [
        Toggle('help', '--help'),

        # Message options
        Prefixed('msg-id', '--msg-id'),
        Prefixed('msg-subject', '--msg-subject'),
        Prefixed('msg-reply-to', '--msg-reply-to'),
        Prefixed('msg-reply-to-group-id', '--msg-reply-to-group-id'),
        Prefixed('msg-durable', '--msg-durable'),
        Prefixed('msg-ttl', '--msg-ttl'),
        Prefixed('msg-priority', '--msg-priority'),
        Prefixed('msg-correlation-id', '--msg-correlation-id'),
        Prefixed('msg-user-id', '--msg-user-id'),
        Prefixed('msg-group-id', '--msg-group-id'),
        Prefixed('msg-group-seq', '--msg-group-seq'),
        MsgProperty('msg-property', '--msg-property'),
        Prefixed('property-type', '--property-type'),
        MsgContentMap('msg-content-map-item', '--msg-content-map-item'),
        MsgContentList('msg-content-list-item', '--msg-content-list-item'),
        Prefixed('msg-content-from-file', '--msg-content-from-file'),
        Prefixed('msg-content', '--msg-content'),
        Prefixed('msg-anotation', '--msg-anotation'),
        Prefixed('msg-content-type', '--msg-content-type'),
        Prefixed('content-type', '--content-type'),

        # Control options
        Prefixed('capacity', '--capacity'),
        Prefixed('reactor-auto-settle-off', '--reactor-auto-settle-off'),
        Prefixed('anonymous', '--anonymous'),
        Prefixed('duration', '--duration'),
        Prefixed('log-msgs', '--log-msgs'),

        Toggle('link-at-most-once', '--link-at-most-once'),
        Toggle('link-at-least-once', '--link-at-least-once'),

        BrokerURLnodeJS('broker-url', '--broker'),
        Prefixed('address', '--address'),
        Prefixed('count', '--count'),
        Prefixed('close-sleep', '--close-sleep'),
        Prefixed('timeout', '--timeout'),
        Prefixed('log-lib', '--log-lib'),
        Prefixed('log-stats', '--log-stats'),
        Toggle('link-durable', '--link-durable'),

        # Connection options
        Prefixed('conn-urls', '--conn-urls'),
        Prefixed('conn-reconnect', '--conn-reconnect'),
        Prefixed('conn-reconnect-interval', '--conn-reconnect-interval'),
        Prefixed('conn-reconnect-limit', '--conn-reconnect-limit'),
        Prefixed('conn-reconnect-timeout', '--conn-reconnect-timeout'),
        Prefixed('conn-heartbeat', '--conn-heartbeat'),
        Prefixed('conn-ssl', '--conn-ssl'),
        Prefixed('conn-ssl-certificate', '--conn-ssl-certificate'),
        Prefixed('conn-ssl-password', '--conn-ssl-password'),
        Prefixed('conn-ssl-trust-store', '--conn-ssl-trust-store'),
        Prefixed('conn-ssl-verify-peer', '--conn-ssl-verify-peer'),
        Prefixed('conn-ssl-verify-peer-name', '--conn-ssl-verify-peer-name'),
        Prefixed('conn-max-frame-size', '--conn-max-frame-size'),
        Prefixed('conn-web-socket', '--conn-web-socket'),

    ]

    def __init__(self, node: Node):
        """Init of NodeJS sender."""

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
