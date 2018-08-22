
"""
Specialized options for external Python Proton client commands (cli-proton-python).
"""
from messaging_abstract.component.client.command.options.client_options import ControlOptionsCommon, \
    ControlOptionsSenderReceiver, ControlOptionsReceiver
from optconstruct.types import Prefixed


class PythonControlOptionsCommon(ControlOptionsCommon):
    """
    Specialized implementation of control options for python client commands.
    """
    def __init__(self, broker_url: str='127.0.0.1:5672', count: int=1,
                 timeout: int=None, sync_mode: str=None, close_sleep: int=None):
        super(PythonControlOptionsCommon, self).__init__(count, timeout, sync_mode, close_sleep)
        self.broker_url = broker_url  # type: str

    def valid_options(self) -> list:
        return ControlOptionsCommon.valid_options(self) + [
            Prefixed('broker-url', '--broker-url')
        ]


class PythonControlOptionsSenderReceiver(ControlOptionsSenderReceiver, PythonControlOptionsCommon):
    """
    Specialized implementation of control options for Sender and Receiver Python client commands.
    """
    def __init__(self, broker_url: str='127.0.0.1:5672/examples', count: int=1,
                 timeout: int=None, sync_mode: str=None, close_sleep: int=None,
                 duration: int=None, duration_mode: str=None, capacity: int=None):
        ControlOptionsSenderReceiver.__init__(self, duration=duration, duration_mode=duration_mode, capacity=capacity)
        PythonControlOptionsCommon.__init__(self, broker_url=broker_url, count=count, timeout=timeout,
                                            sync_mode=sync_mode, close_sleep=close_sleep)


class PythonControlOptionsReceiver(ControlOptionsReceiver, PythonControlOptionsSenderReceiver):
    """
    Specialized implementation of control options for Receiver Python client command.
    """
    def __init__(self, broker_url: str='127.0.0.1:5672/examples', count: int=1,
                 timeout: int=None, sync_mode: str=None, duration: int=None,
                 duration_mode: str=None, capacity: int=None, dynamic: bool=False):
        ControlOptionsReceiver.__init__(self, dynamic=dynamic)
        PythonControlOptionsSenderReceiver.__init__(self, broker_url=broker_url, count=count,
                                                  timeout=timeout, sync_mode=sync_mode, duration=duration,
                                                  duration_mode=duration_mode, capacity=capacity)
