from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Sender, Message, Node

from messaging_components.clients.external.java.client import ClientJava
from messaging_components.clients.external.java.command.java_commands import JavaSenderClientCommand

try:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import urlparse, urlunparse, quote, unquote


@logged
@traced
class SenderJava(Sender, ClientJava):
    """External Java Qpid JMS sender client."""

    _command: JavaSenderClientCommand

    def set_url(self, url: str):
        p_url = urlparse(url)
        self._command.control.broker = urlunparse((p_url.scheme or '', p_url.netloc or '', '', '', '', ''))
        self._command.control.address = urlunparse(('', '', p_url.path or '', p_url.params or '',
                                                    p_url.query or '', p_url.fragment or ''))

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> JavaSenderClientCommand:
        return JavaSenderClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                       timeout=timeout, encoding=encoding)

    def _send(self, message: Message, **kwargs):
        self._command.message.msg_content = message.body
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderJava, self).__init__(name, node, executor)
