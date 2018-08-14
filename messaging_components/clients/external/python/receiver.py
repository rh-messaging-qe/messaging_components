"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from .opt.brokerurl import BrokerURLPythonProton
from optconstruct.types.prefixed import Prefixed
from optconstruct.types import Toggle

import messaging_abstract.client
from .client import Client
from messaging_components.node.node import Node


@logged
@traced
class Receiver(Client, messaging_abstract.client.Receiver):
    """External Python-Proton receiver client."""

    # client is installed from cli-rhea
    cli_command = ['cli-proton-python-receiver']

    cli_params_transformation = [
        Toggle('help', '--help'),
        # Control options
        BrokerURLPythonProton('broker-url', '--broker-url'),
        Prefixed('count', '--count'),
        Prefixed('timeout', '--timeout'),
        Prefixed('close-sleep', '--close-sleep'),
        Prefixed('sync-mode', '--sync-mode'),
        Prefixed('duration', '--duration'),
        Prefixed('duration-mode', '--duration-mode'),
        Prefixed('capacity', '--capacity'),
        Toggle('dynamic', '--dynamic'),

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
        Prefixed('conn-reconnect-interval', '--conn-reconnect-interval'),
        Prefixed('conn-reconnect-limit', '--conn-reconnect-limit'),
        Prefixed('conn-reconnect-timeout', '--conn-reconnect-timeout'),
        Prefixed('conn-heartbeat', '--conn-heartbeat'),
        Prefixed('conn-ssl-domain-certificate', '--conn-ssl-certificate'),
        Prefixed('conn-ssl-domain-private-key', '--conn-ssl-private-key'),
        Prefixed('conn-ssl-domain-password', '--conn-ssl-password'),
        Prefixed('conn-ssl-domain-trust-store', '--conn-ssl-trust-store'),
        Prefixed('conn-ssl-domain-verify-peer', '--conn-ssl-verify-peer'),
        Prefixed('conn-ssl-domain-verify-peer-name', '--conn-ssl-verify-peer-name'),
        Prefixed('conn-handler', '--conn-handler'),
        Prefixed('conn-max-frame-size', '--conn-max-frame-size'),

        # Link options
        Toggle('link-durable', '--link-durable'),
        Toggle('link-at-least-once', '--link-at-least-once'),
        Toggle('link-at-most-once', '--link-at-most-once'),
        Prefixed('link-dynamic-node-properties', '--link-dynamic-node-properties'),

        # Receiver options
        Prefixed('process-reply-to', '--process-reply-to'),
        Prefixed('action', '--action'),
        Prefixed('action-size', '--action-size'),
        Prefixed('recv-selector', '--recv-selector'),
        Toggle('recv-browse', '--recv-browse'),
        Toggle('recv-consume', '--recv-consume'),
        Prefixed('recv-filter', '--recv-filter'),
        Toggle('recv-listen', '--recv-listen'),

        # Reactor options
        Prefixed('reactor-prefetch', '--reactor-prefetch'),
        Toggle('reactor-auto-accept', '--reactor-auto-accept'),
        Toggle('reactor-peer-close-is-error', '--reactor-peer-close-is-error'),
        Toggle('reactor-auto-settle-off', '--reactor-auto-settle-off'),

    ]

    def __init__(self, node: Node):
        """Init Python receiver."""

        messaging_abstract.client.Receiver.__init__(self)
        Client.__init__(self, node)
