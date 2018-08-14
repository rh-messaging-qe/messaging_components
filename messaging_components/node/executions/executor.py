# @TODO implement @mlesko Executor

from autologging import logged, traced
from .execution import Execution


@logged
@traced
class Executor(Execution):
    def __init__(self, hostname):
        Execution.__init__(self, hostname=hostname)
