from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.server.router import Router
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node

from .management import QDManage, QDStat
from .config import Config
from .log import Log


@logged
@traced
class Dispatch(Router):
    """
    Dispatch router component
    """

    name = 'Qpid Dispatch Router'

    def __init__(self, name: str, node: Node, executor: Executor, service: Service, port=5672, config=None):
        super(Dispatch, self).__init__(name, node, executor, service)

        self.qdmanage = QDManage()
        self.qdstat = QDStat()
        self.config = Config()  # TODO - pass config as param to constructor
        self.log = Log()
        self._version = None

    @staticmethod
    def config_refresh_remote_to_testsuite():
        # TODO - This seems like a candidate to be part of Config class
        """
        Syncing router config from remote to test_suite
        :return:
        """
        pass

    @staticmethod
    def config_dump():
        # TODO - This seems like a candidate to be part of Config class
        """
        Dump (remote) router configuration file and create Config()
        :return:
        """

    def set_config(self, config_src, config_dst):
        # TODO - Need to describe the purpose of this method (unclear at the moment)
        """
        Set configuration from
        :param config_src:
        :param config_dst:
        :return:
        """

    @property
    def version(self):
        """
        Get qdrouterd version
        :return:
        """
        if self._version:
            return self._version
        else:
            cmd = self.node.execute(['qdrouterd', '-v'])
            return cmd
