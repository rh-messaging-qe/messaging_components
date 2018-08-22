from autologging import logged, traced
from iqa_common.executor import Executor
from messaging.client.command.impl import JavaConnectorClientCommand
from messaging_abstract.component.client import Connector, Node

from messaging_components.clients.external.java.client import ClientJava


@logged
@traced
class ConnectorJava(Connector, ClientJava):
    """External Java Qpid JMS connector client."""

    def new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> JavaConnectorClientCommand:
        return JavaConnectorClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                          timeout=timeout, encoding=encoding)

    def connect(self) -> bool:
        self.execution = self.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ConnectorJava, self).__init__(name, node, executor)
