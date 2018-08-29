"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from messaging_abstract.component.client import Sender, Node, Executor, ClientCommand
from messaging_abstract.message import Message

from messaging_components.clients.external.python.client import ClientPython
from messaging_components.clients.external.python.command.python_commands import PythonSenderClientCommand


@logged
@traced
class SenderPython(Sender, ClientPython):
    """External Python-Proton sender client."""

    # Just to enforce implementation being used
    _command: PythonSenderClientCommand

    def set_url(self, url: str):
        self._command.control.broker_url = url

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> ClientCommand:
        return PythonSenderClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                         timeout=timeout, encoding=encoding)

    def _send(self, message: Message, **kwargs):
        self._command.message.msg_content = message.body
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderPython, self).__init__(name, node, executor)
