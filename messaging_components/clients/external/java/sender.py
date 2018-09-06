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
        self._command.control.broker = '{}://{}:{}'.\
            format(p_url.scheme or 'amqp', p_url.hostname or '127.0.0.1', p_url.port or '5672')
        self._command.control.address = urlunparse(('', '', p_url.path or '', p_url.params or '',
                                                    p_url.query or '', p_url.fragment or ''))

        # Java client expects unquoted username and passwords
        if p_url.username:
            self._command.connection.conn_username = unquote(p_url.username)
        if p_url.password:
            self._command.connection.conn_password = unquote(p_url.password)

    def set_auth_mechs(self, mechs: str):
        self._command.connection.conn_auth_mechanisms = mechs

    def _new_command(self, stdout: bool = True, stderr: bool = True, daemon: bool = True,
                     timeout: int = ClientJava.TIMEOUT, encoding: str = "utf-8") -> JavaSenderClientCommand:
        return JavaSenderClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                       timeout=timeout, encoding=encoding)

    def _send(self, message: Message, **kwargs):
        self._command.message.msg_content = message.body
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(SenderJava, self).__init__(name, node, executor)
