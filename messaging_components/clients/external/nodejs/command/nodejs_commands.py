
"""
Specialized implementation of external command for cli-rhea clients (NodeJS). 
"""
from messaging_abstract.component.client.command.client_command import ConnectorClientCommand, ReceiverClientCommand, \
    SenderClientCommand
from messaging_abstract.component.client.command.options.client_options import LinkOptionsSenderReceiver, \
    ReactorOptionsSenderReceiver

from messaging_components.clients.external.nodejs.command.nodejs_options import NodeJSControlOptionsCommon, \
    NodeJSControlOptionsReceiver, NodeJSControlOptionsSenderReceiver


class NodeJSConnectorClientCommand(ConnectorClientCommand):
    """
    CLI RHEA connector client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """
    def __init__(self, stdout: bool=False, stderr: bool=False,
                   daemon: bool=False, timeout: int=0,
                   encoding: str="utf-8"):
        super(NodeJSConnectorClientCommand, self).__init__(stdout, stderr, daemon, timeout, encoding)
        self.control = NodeJSControlOptionsCommon()

    def main_command(self) -> list:
        return ['cli-rhea-connector']


class NodeJSReceiverClientCommand(ReceiverClientCommand):
    """
    CLI RHEA receiver client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """
    def __init__(self, stdout: bool=False, stderr: bool=False,
                   daemon: bool=False, timeout: int=0,
                   encoding: str="utf-8"):
        super(NodeJSReceiverClientCommand, self).__init__(stdout, stderr, daemon, timeout, encoding)
        self.control = NodeJSControlOptionsReceiver()
        self.link = LinkOptionsSenderReceiver()
        self.reactor = ReactorOptionsSenderReceiver()

    def main_command(self) -> list:
        return ['cli-rhea-receiver']


class NodeJSSenderClientCommand(SenderClientCommand):
    """
    CLI RHEA sender client command specialization.
    In Node JS client we must provide --broker and (optionally) --address.
    The control property instance used here is RHEAControlOptionsCommon.
    """
    def __init__(self, stdout: bool=False, stderr: bool=False,
                   daemon: bool=False, timeout: int=0,
                   encoding: str="utf-8"):
        super(NodeJSSenderClientCommand, self).__init__(stdout, stderr, daemon, timeout, encoding)
        self.control = NodeJSControlOptionsSenderReceiver()
        self.link = LinkOptionsSenderReceiver()
        self.reactor = ReactorOptionsSenderReceiver()

    def main_command(self) -> list:
        return ['cli-rhea-sender']
