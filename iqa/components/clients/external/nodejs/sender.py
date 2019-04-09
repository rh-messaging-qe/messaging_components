"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Sender, Node
from messaging_abstract.message import Message

from messaging_components.clients.external.nodejs.client import ClientNodeJS
from messaging_components.clients.external.nodejs.command.nodejs_commands import NodeJSSenderClientCommand

try:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import urlparse, urlunparse, quote, unquote


@logged
@traced
class SenderNodeJS(Sender, ClientNodeJS):
    """External NodeJS sender client."""

    _command: NodeJSSenderClientCommand

    def _set_url(self, url: str):
        p_url = urlparse(url)
        p_url._replace(scheme=None)
        self._command.control.broker = p_url.netloc
        self._command.control.address = urlunparse(('', '', p_url.path or '', p_url.params or '',
                                                    p_url.query or '', p_url.fragment or ''))

    def set_auth_mechs(self, mechs: str):
        pass

    def set_ssl_auth(self, pem_file: str = None, key_file: str = None, keystore: str = None, keystore_pass: str = None,
                     keystore_alias: str = None):
        self._command.connection.conn_ssl_certificate = pem_file
        self._command.connection.conn_ssl_private_key = key_file
        self._command.connection.conn_ssl = True

    def _new_command(self, stdout: bool = True, stderr: bool = True, daemon: bool = True,
                     timeout: int = ClientNodeJS.TIMEOUT, encoding: str = "utf-8") -> NodeJSSenderClientCommand:
        return NodeJSSenderClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                         timeout=timeout, encoding=encoding)

    def _send(self, message: Message, **kwargs):
        self._command.message.msg_content = message.body
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(SenderNodeJS, self).__init__(name, node, executor, **kwargs)
