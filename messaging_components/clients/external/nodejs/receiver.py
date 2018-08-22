"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Receiver, Node

from messaging_components.clients.external.nodejs.client import ClientNodeJS
from messaging_components.clients.external.nodejs.command.nodejs_commands import NodeJSReceiverClientCommand


@logged
@traced
class ReceiverNodeJS(Receiver, ClientNodeJS):
    """External NodeJS receiver client."""

    def new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> NodeJSReceiverClientCommand:
        return NodeJSReceiverClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                           timeout=timeout, encoding=encoding)

    def receive(self):
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverNodeJS, self).__init__(name, node, executor)
