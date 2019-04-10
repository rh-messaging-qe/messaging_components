"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from iqa.components.clients.external.python.command.python_commands import PythonConnectorClientCommand
from iqa.system.node import Node, Executor
from .client import ClientPython


@logged
@traced
class ConnectorPython(ClientPython):
    """External Python-Proton connector client."""

    _command: PythonConnectorClientCommand

    def _set_url(self, url: str):
        self._command.control.broker_url = url

    def set_auth_mechs(self, mechs: str):
        self._command.connection.conn_allowed_mechs = mechs

    def set_ssl_auth(self, pem_file: str = None, key_file: str = None, keystore: str = None, keystore_pass: str = None,
                     keystore_alias: str = None):
        self._command.connection.conn_ssl_certificate = pem_file
        self._command.connection.conn_ssl_private_key = key_file

    def _new_command(self, stdout: bool = True, stderr: bool = True, daemon: bool = True,
                     timeout: int = ClientPython.TIMEOUT, encoding: str = "utf-8") -> PythonConnectorClientCommand:
        return PythonConnectorClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                            timeout=timeout, encoding=encoding)

    def connect(self) -> bool:
        self.execution = self.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ConnectorPython, self).__init__(name, node, executor, **kwargs)
