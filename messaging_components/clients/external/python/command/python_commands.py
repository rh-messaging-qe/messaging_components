
"""
Implementation of cli-proton-python external client command.
"""
from messaging_components.clients.external.command.client_command import ConnectorClientCommand, ReceiverClientCommand, \
    LinkOptionsReceiver, ReactorOptionsSenderReceiver, SenderClientCommand, LinkOptionsSenderReceiver
from messaging_components.clients.external.python.command.python_options import PythonControlOptionsCommon, \
    PythonControlOptionsReceiver, PythonControlOptionsSenderReceiver, PythonConnectionOptionsCommon, \
    PythonControlOptionsSender


class PythonConnectorClientCommand(ConnectorClientCommand):
    """
    Connector client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
    """
    def __init__(self, stdout: bool=False, stderr: bool=False, daemon: bool=False,
                 timeout: int=0, encoding: str="utf-8"):
        super(PythonConnectorClientCommand, self).__init__(stdout, stderr, daemon, timeout, encoding)
        self.control = PythonControlOptionsCommon()
        self.connection = PythonConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-proton-python-connector']


class PythonReceiverClientCommand(ReceiverClientCommand):
    """
    Receiver client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
    """
    def __init__(self, stdout: bool=False, stderr: bool=False, daemon: bool=False,
                 timeout: int=0, encoding: str="utf-8"):
        super(PythonReceiverClientCommand, self).__init__(stdout, stderr, daemon, timeout, encoding)
        self.control = PythonControlOptionsReceiver()
        self.link = LinkOptionsReceiver()
        self.reactor = ReactorOptionsSenderReceiver()
        self.connection = PythonConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-proton-python-receiver']


class PythonSenderClientCommand(SenderClientCommand):
    """
    Sender client command for cli-proton-python.
    In Python client there is --broker-url parameter and so we need
    to replace control instance by PythonControlOptionsCommon.
    """
    def __init__(self, stdout: bool=False, stderr: bool=False, daemon: bool=False,
                 timeout: int=0, encoding: str="utf-8"):
        super(PythonSenderClientCommand, self).__init__(stdout, stderr, daemon, timeout, encoding)
        self.control = PythonControlOptionsSender()
        self.link = LinkOptionsSenderReceiver()
        self.reactor = ReactorOptionsSenderReceiver()
        self.connection = PythonConnectionOptionsCommon()

    def main_command(self) -> list:
        return ['cli-proton-python-sender']
