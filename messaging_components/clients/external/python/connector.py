"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Connector, Node

from messaging_components.clients.external.python.command.python_commands import PythonConnectorClientCommand
from .client import ClientPython


@logged
@traced
class ConnectorPython(Connector, ClientPython):
    """External Python-Proton connector client."""

    _command: PythonConnectorClientCommand

    def set_url(self, url: str):
        self._command.control.broker_url(url)

    def set_auth_mechs(self, mechs: str):
        self._command.connection.conn_allowed_mechs = mechs

    def _new_command(self, stdout: bool = True, stderr: bool = True, daemon: bool = True,
                     timeout: int = ClientPython.TIMEOUT, encoding: str = "utf-8") -> PythonConnectorClientCommand:
        return PythonConnectorClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                            timeout=timeout, encoding=encoding)

    def connect(self) -> bool:
        self.execution = self.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ConnectorPython, self).__init__(name, node, executor)
