"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Receiver
from messaging_abstract.node.node import Node

from messaging_components.clients.external.python.command.python_commands import PythonReceiverClientCommand
from .client import ClientPython


@logged
@traced
class ReceiverPython(Receiver, ClientPython):
    """External Python-Proton receiver client."""

    _command: PythonReceiverClientCommand

    def set_url(self, url: str):
        self._command.control.broker_url = url

    def set_auth_mechs(self, mechs: str):
        self._command.connection.conn_allowed_mechs = mechs

    def set_ssl_auth(self, pem_file: str = None, key_file: str = None, keystore: str = None, keystore_pass: str = None,
                     keystore_alias: str = None):
        self._command.connection.conn_ssl_certificate = pem_file
        self._command.connection.conn_ssl_private_key = key_file

    def _new_command(self, stdout: bool = True, stderr: bool = True, daemon: bool = True,
                     timeout: int = ClientPython.TIMEOUT, encoding: str = "utf-8") -> PythonReceiverClientCommand:
        return PythonReceiverClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                           timeout=timeout, encoding=encoding)

    def receive(self):
        self._command.control.timeout = self.command.timeout
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverPython, self).__init__(name, node, executor)
