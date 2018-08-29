from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Connector, Node

from messaging_components.clients.external.java.client import ClientJava
from messaging_components.clients.external.java.command.java_commands import JavaConnectorClientCommand

try:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import urlparse, urlunparse, quote, unquote


@logged
@traced
class ConnectorJava(Connector, ClientJava):
    """External Java Qpid JMS connector client."""

    _command: JavaConnectorClientCommand

    def set_url(self, url: str):
        p_url = urlparse(url)
        self._command.control.broker = urlunparse((p_url.scheme or '', p_url.netloc or ''))
        self._command.control.address = urlunparse((p_url.path or '', p_url.params or '',
                                                    p_url.query or '', p_url.fragment or ''))

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                    encoding: str = "utf-8") -> JavaConnectorClientCommand:
        return JavaConnectorClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                          timeout=timeout, encoding=encoding)

    def connect(self) -> bool:
        self.execution = self.execute(self.command)
        if self.execution.completed_successfully():
            return True
        return False

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ConnectorJava, self).__init__(name, node, executor)
