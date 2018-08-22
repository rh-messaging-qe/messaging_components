
"""
Specialized options for external Node JS client commands (cli-rhea).
"""
from messaging_abstract.component.client.command.options.client_options import ControlOptionsCommon, \
    ControlOptionsSenderReceiver, ControlOptionsReceiver
from optconstruct.types import Prefixed


class NodeJSControlOptionsCommon(ControlOptionsCommon):
    """
    Specialized implementation of control options for cli-rhea client commands.
    """
    def __init__(self, broker: str='localhost:5672', count: int=1,
                 timeout: int=None, sync_mode: str=None, close_sleep: int=None):
        super(NodeJSControlOptionsCommon, self).__init__(count, timeout, sync_mode, close_sleep)
        self.broker = broker  # type: str

    def valid_options(self) -> list:
        return super(NodeJSControlOptionsCommon, self).valid_options() + [
            Prefixed('broker', '--broker')
        ]


class NodeJSControlOptionsSenderReceiver(ControlOptionsSenderReceiver, NodeJSControlOptionsCommon):
    """
    Specialized implementation of control options for cli-rhea Sender and Receiver client commands.
    """
    def __init__(self, broker: str='localhost:5672', address: str='examples', count: int=1,
                 timeout: int=None, sync_mode: str=None, close_sleep: int=None,
                 duration: int=None, duration_mode: str=None, capacity: int=None):
        ControlOptionsSenderReceiver.__init__(self, duration=duration, duration_mode=duration_mode,
                                              capacity=capacity)
        NodeJSControlOptionsCommon.__init__(self, broker=broker, count=count, timeout=timeout,
                                          sync_mode=sync_mode, close_sleep=close_sleep)
        self.address = address  # type: str

    def valid_options(self) -> list:
        return NodeJSControlOptionsCommon.valid_options(self) + [
            Prefixed('address', '--address')
        ]


class NodeJSControlOptionsReceiver(ControlOptionsReceiver, NodeJSControlOptionsSenderReceiver):
    """
    Specialized implementation of control options for cli-rhea Receiver client command.
    """
    def __init__(self, broker: str='localhost:5672/examples', count: int=1,
                 timeout: int=None, sync_mode: str=None,
                 duration: int=None, duration_mode: str=None, capacity: int=None,
                 dynamic: bool=False):
        ControlOptionsReceiver.__init__(self, dynamic=dynamic)
        NodeJSControlOptionsSenderReceiver.__init__(self, broker=broker, count=count, timeout=timeout,
                                                  sync_mode=sync_mode, duration=duration,
                                                  duration_mode=duration_mode, capacity=capacity)
