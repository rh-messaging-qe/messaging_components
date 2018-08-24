"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Sender, Node
from messaging_abstract.message import Message

from messaging_components.clients.external.nodejs.client import ClientNodeJS
from messaging_components.clients.external.nodejs.command.nodejs_commands import NodeJSSenderClientCommand


@logged
@traced
class SenderNodeJS(Sender, ClientNodeJS):
    """External NodeJS sender client."""

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> NodeJSSenderClientCommand:
        return NodeJSSenderClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                         timeout=timeout, encoding=encoding)

    def _send(self, message: Message, **kwargs):
        # TODO Store message in Filesystem and use it as an argument
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderNodeJS, self).__init__(name, node, executor)
