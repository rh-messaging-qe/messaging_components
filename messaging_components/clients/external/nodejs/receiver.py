"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from .opt.brokerurl import BrokerURLnodeJS
from optconstruct.types.prefixed import Prefixed
from optconstruct.types import Toggle

import messaging_abstract.client
from messaging_components.node.node import Node
from .client import Client


@logged
@traced
class Receiver(Client, messaging_abstract.client.Receiver):
    """External NodeJS receiver client."""
    # client is installed from cli-rhea, node_app is there only for backward compatibility
    cli_command = ['cli-rhea-receiver']

    # Client-sender params for build execute command
    cli_params_transformation = [
        Toggle('help', '--help'),
        # Control options
        Prefixed('recv-msg-selector', '--recv-selector'),
        Toggle('recv-browse', '--recv-browse'),
        Prefixed('action', '--action'),
        Prefixed('capacity', '--capacity'),
        Toggle('process-reply-to', '--process-reply-to'),
        Prefixed('recv-listen', '--recv-listen'),
        Prefixed('recv-listen-port', '--recv-listen-port'),
        Prefixed('duration', '--duration'),

        BrokerURLnodeJS('broker-url', '--broker'),
        Prefixed('address', '--address'),
        Prefixed('count', '--count'),
        Prefixed('close-sleep', '--close-sleep'),
        Prefixed('timeout', '--timeout'),

        # Logging options
        Prefixed('log-msgs', '--log-msgs'),
        Prefixed('log-lib', '--log-lib'),
        Prefixed('log-stats', '--log-stats'),

        # Link options
        Toggle('link-at-most-once', '--link-at-most-once'),
        Toggle('link-at-least-once', '--link-at-least-once'),
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
        """Init of NodeJS receiver."""

        messaging_abstract.client.Receiver.__init__(self)
        Client.__init__(self, node)
