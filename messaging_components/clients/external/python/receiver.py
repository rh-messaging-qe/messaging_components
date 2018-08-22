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

    def new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> PythonReceiverClientCommand:
        return PythonReceiverClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                           timeout=timeout, encoding=encoding)

    def receive(self):
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverPython, self).__init__(name, node, executor)
