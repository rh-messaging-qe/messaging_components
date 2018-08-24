"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Connector, Node

from messaging_components.clients.external.nodejs.command.nodejs_commands import NodeJSConnectorClientCommand
from .client import ClientNodeJS


@logged
@traced
class ConnectorNodeJS(Connector, ClientNodeJS):
    """External NodeJS connector client."""

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> NodeJSConnectorClientCommand:
        return NodeJSConnectorClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                            timeout=timeout, encoding=encoding)

    def connect(self) -> bool:
        self.execution = self.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ConnectorNodeJS, self).__init__(name, node, executor)
