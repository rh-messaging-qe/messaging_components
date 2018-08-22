from autologging import logged, traced
from iqa_common.executor import Executor
from messaging.client.command.impl import JavaReceiverClientCommand
from messaging_abstract.component.client import Receiver, Node

from messaging_components.clients.external.java.client import ClientJava


@logged
@traced
class ReceiverJava(Receiver, ClientJava):
    """External Java Qpid JMS receiver client."""

    def new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> JavaReceiverClientCommand:
        return JavaReceiverClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                         timeout=timeout, encoding=encoding)

    def receive(self):
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverJava, self).__init__(name, node, executor)
