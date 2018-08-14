"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from messaging_components.node import Node
from .opt.brokerurl import BrokerURLnodeJS
from optconstruct.types.prefixed import Prefixed
from optconstruct.types import Toggle

import messaging_abstract.client
from .client import Client


@logged
@traced
class Connector(Client, messaging_abstract.client.Connector):
    """External NodeJS connector client."""

    # client is installed from cli-rhea, node_app is there only for backward compatibility
    cli_command = ['cli-rhea-connector']

    cli_params_transformation = [
        Toggle('help', '--help'),
        Prefixed('obj-ctrl', '--obj-ctrl'),
        # Control options
        BrokerURLnodeJS('broker-url', '--broker'),
        Prefixed('address', '--address'),
        Prefixed('count', '--count'),
        Prefixed('close-sleep', '--close-sleep'),
        Prefixed('timeout', '--timeout'),

        # Logging options
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
        Prefixed('conn-ssl-private-key', '--conn-ssl-private-key'),
        Prefixed('conn-ssl-password', '--conn-ssl-password'),
        Prefixed('conn-ssl-trust-store', '--conn-ssl-trust-store'),
        Toggle('conn-ssl-verify-peer', '--conn-ssl-verify-peer'),
        Toggle('conn-ssl-verify-peer-name', '--conn-ssl-verify-peer-name'),
        Prefixed('conn-max-frame-size', '--conn-max-frame-size'),
        Prefixed('conn-web-socket', '--conn-web-socket'),

    ]

    def __init__(self, node: Node):
        """Init of NodeJS connector."""

        messaging_abstract.client.Connector.__init__(self)
        Client.__init__(self, node)
