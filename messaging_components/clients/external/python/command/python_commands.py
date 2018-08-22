
"""
Implementation of cli-proton-python external client command.
"""
from messaging_abstract.component.client.command.client_command import ConnectorClientCommand, ReceiverClientCommand, \
    SenderClientCommand

from messaging_components.clients.external.python.command.python_options import PythonControlOptionsCommon, \
    PythonControlOptionsReceiver, PythonControlOptionsSenderReceiver


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
        self.control = PythonControlOptionsSenderReceiver()

    def main_command(self) -> list:
        return ['cli-proton-python-sender']
