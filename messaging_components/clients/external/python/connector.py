"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from messaging_components.node import Node
from .opt.brokerurl import BrokerURLPythonProton
from optconstruct.types.prefixed import Prefixed
from optconstruct.types import Toggle

import messaging_abstract.client
from .client import Client


@logged
@traced
class Connector(Client, messaging_abstract.client.Connector):
    """External Python-Proton connector client."""

    # client is installed from cli-rhea, node_app is there only for backward compatibility
    cli_command = ['cli-proton-python-connector']

    cli_params_transformation = [
        Toggle('help', '--help'),
        # Control options
        BrokerURLPythonProton('broker-url', '--broker-url'),
        Prefixed('count', '--count'),
        Prefixed('timeout', '--timeout'),
        Prefixed('close-sleep', '--close-sleep'),
        Prefixed('sync-mode', '--sync-mode'),

        # Logging options
        Prefixed('log-lib', '--log-lib'),
        Prefixed('log-stats', '--log-stats'),

        # Connection options
        Prefixed('conn-urls', '--conn-urls'),
        Prefixed('conn-reconnect', '--conn-reconnect'),
        Prefixed('conn-reconnect-interval', '--conn-reconnect-interval'),
        Prefixed('conn-reconnect-limit', '--conn-reconnect-limit'),
        Prefixed('conn-reconnect-timeout', '--conn-reconnect-timeout'),
        Prefixed('conn-heartbeat', '--conn-heartbeat'),
        Prefixed('conn-ssl-certificate', '--conn-ssl-certificate'),
        Prefixed('conn-ssl-password', '--conn-ssl-password'),
        Prefixed('conn-ssl-trust-store', '--conn-ssl-trust-store'),
        Toggle('conn-ssl-verify-peer', '--conn-ssl-verify-peer'),
        Toggle('conn-ssl-verify-peer-name', '--conn-ssl-verify-peer-name'),
        Prefixed('conn-handler', '--conn-handler'),
        Prefixed('conn-max-frame-size', '--conn-max-frame-size'),

        # Connector options
        Prefixed('obj-ctrl', '--obj-ctrl'),

    ]

    def __init__(self, node: Node):
        """Init of Python connector."""

        messaging_abstract.client.Connector.__init__(self)
        Client.__init__(self, node)
