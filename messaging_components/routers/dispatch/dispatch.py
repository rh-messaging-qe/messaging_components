from autologging import logged, traced

from messaging_components.routers import Router
from messaging_components.node.service import Service
from messaging_components.node import Node

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

    def __init__(self, node: Node, service='qdrouterd'):
        Router.__init__(self, node=node)
        self.qdmanage = QDManage()
        self.qdstat = QDStat()

        self.config = Config()
        self.log = Log()

        self.service = Service(node, service)
        self._version = None

    @staticmethod
    def config_refresh_remote_to_testsuite():
        """
        Syncing router config from remote to test_suite
        :return:
        """
        pass

    @staticmethod
    def config_dump():
        """
        Dump (remote) router configuration file and create Config()
        :return:
        """

    def set_config(self, config_src, config_dst):
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
