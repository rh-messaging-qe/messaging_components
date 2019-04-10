"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced

from iqa.components.clients.external.nodejs.command.nodejs_commands import NodeJSConnectorClientCommand
from iqa.system.node import Node, Executor
from .client import ClientNodeJS

try:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import urlparse, urlunparse, quote, unquote


@logged
@traced
class ConnectorNodeJS(ClientNodeJS):
    """External NodeJS connector client."""

    _command: NodeJSConnectorClientCommand

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
                     timeout: int = ClientNodeJS.TIMEOUT, encoding: str = "utf-8") -> NodeJSConnectorClientCommand:
        return NodeJSConnectorClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                            timeout=timeout, encoding=encoding)

    def connect(self) -> bool:
        self.execution = self.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ConnectorNodeJS, self).__init__(name, node, executor, **kwargs)
