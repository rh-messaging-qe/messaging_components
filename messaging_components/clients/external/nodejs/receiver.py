"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Receiver, Node

from messaging_components.clients.external.nodejs.client import ClientNodeJS
from messaging_components.clients.external.nodejs.command.nodejs_commands import NodeJSReceiverClientCommand

try:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import urlparse, urlunparse, quote, unquote


@logged
@traced
class ReceiverNodeJS(Receiver, ClientNodeJS):
    """External NodeJS receiver client."""

    _command: NodeJSReceiverClientCommand

    def set_url(self, url: str):
        p_url = urlparse(url)
        p_url._replace(scheme=None)
        self._command.control.broker = p_url.netloc
        self._command.control.address = urlunparse(('', '', p_url.path or '', p_url.params or '',
                                                    p_url.query or '', p_url.fragment or ''))

    def set_auth_mechs(self, mechs: str):
        pass

    def _new_command(self, stdout: bool = True, stderr: bool = True, daemon: bool = True,
                     timeout: int = ClientNodeJS.TIMEOUT, encoding: str = "utf-8") -> NodeJSReceiverClientCommand:
        return NodeJSReceiverClientCommand(stdout=stdout, stderr=stderr, daemon=daemon,
                                           timeout=timeout, encoding=encoding)

    def receive(self):
        self._command.control.timeout = self.command.timeout
        self.execution = self.execute(self.command)

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ReceiverNodeJS, self).__init__(name, node, executor)
