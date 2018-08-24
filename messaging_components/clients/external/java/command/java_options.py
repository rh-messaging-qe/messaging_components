from messaging_abstract.component.client.command.options.client_options import ControlOptionsCommon, \
    ControlOptionsSenderReceiver, ControlOptionsReceiver
from optconstruct import OptionAbstract
from optconstruct.types import Toggle, Prefixed, KWOption, ListOption

"""
Specialized options for external Java client commands (cli-qpid.jar).
"""


class JavaControlOptionsCommon(ControlOptionsCommon):
    """
    Specialized implementation of control options for java client commands.
    """
    def __init__(self, broker: str='127.0.0.1:5672', count: int=1,
                 timeout: int=None, sync_mode: str=None, close_sleep: int=None):
        super(JavaControlOptionsCommon, self).__init__(count, timeout, sync_mode, close_sleep)
        self.broker = broker

    def valid_options(self) -> list:
        return ControlOptionsCommon.valid_options(self) + [
            Prefixed('broker', '--broker')
        ]


class JavaControlOptionsSenderReceiver(ControlOptionsSenderReceiver, JavaControlOptionsCommon):
    """
    Specialized implementation of control options for Sender and Receiver Java client commands.
    """
    def __init__(self, broker: str='127.0.0.1:5672', address: str='examples', count: int=1,
                 timeout: int=None, sync_mode: str=None, close_sleep: int=None,
                 duration: int=None, duration_mode: str=None, capacity: int=None):
        ControlOptionsSenderReceiver.__init__(self, duration=duration, duration_mode=duration_mode, capacity=capacity)
        JavaControlOptionsCommon.__init__(self, broker=broker, count=count, timeout=timeout,
                                          sync_mode=sync_mode, close_sleep=close_sleep)
        self.address = address  # type: str

    def valid_options(self) -> list:
        return JavaControlOptionsCommon.valid_options(self) + [
            Prefixed('address', '--address')
        ]


class JavaControlOptionsReceiver(ControlOptionsReceiver, JavaControlOptionsSenderReceiver):
    """
    Specialized implementation of control options for Receiver Java client command.
    """
    def __init__(self, broker: str='127.0.0.1:5672', address: str='examples', count: int=1,
                 timeout: int=None, sync_mode: str=None, duration: int=None,
                 duration_mode: str=None, capacity: int=None, dynamic: bool=False):
        ControlOptionsReceiver.__init__(self, dynamic=dynamic)
        JavaControlOptionsSenderReceiver.__init__(self, broker=broker, address=address, count=count,
                                                  timeout=timeout, sync_mode=sync_mode, duration=duration,
                                                  duration_mode=duration_mode, capacity=capacity)

    def valid_options(self) -> list:
        return JavaControlOptionsSenderReceiver.valid_options(self) + [
            Toggle('dynamic', '--dynamic')
        ]
