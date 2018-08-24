from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Sender, Message, Node

from messaging_components.clients.external.java.client import ClientJava
from messaging_components.clients.external.java.command.java_commands import JavaSenderClientCommand


@logged
@traced
class SenderJava(Sender, ClientJava):
    """External Java Qpid JMS sender client."""

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> JavaSenderClientCommand:
        return JavaSenderClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                       timeout=timeout, encoding=encoding)

    def _send(self, message: Message, **kwargs):
        # TODO Store message in Filesystem and use it as an argument
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderJava, self).__init__(name, node, executor)
