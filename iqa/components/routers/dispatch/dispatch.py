from autologging import logged, traced

from iqa.abstract.components.server.server_component import ServerComponent
from iqa.abstract.messaging.server.router import Router
from .management import QDManage, QDStat
from .config import Config
from .log import Log


@logged
@traced
class Dispatch(Router, ServerComponent):
    """
    Dispatch router component
    """

    name = 'Qpid Dispatch Router'
    implementation = 'dispatch'

    def __init__(self, name: str, **kwargs):
        super(Dispatch, self).__init__(name, **kwargs)

        self.qdmanage = QDManage()
        self.qdstat = QDStat()
        self.config = Config()  # TODO - pass config as param to constructor
        self.log = Log()
        self._version = None

        self.port = kwargs.get('router_port', 5672)
        self.config = kwargs.get('router_config', None)
        self.user = None
        self.password = None
        self.pem_file = None
        self.key_file = None
        self.key_password = None

        # initializing client from kwargs
        for func in [self.set_credentials, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    @staticmethod
    def config_refresh_remote_to_testsuite():
        # TODO - This seems like a candidate to be part of Configuration class
        """
        Syncing router config from remote to test_suite
        :return:
        """
        pass

    @staticmethod
    def config_dump():
        # TODO - This seems like a candidate to be part of Configuration class
        """
        Dump (remote) router configuration file and create Configuration()
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


    def set_credentials(self, user: str=None, password: str=None):
        """
        Stores user and password that must be used to communicate with the router instance
        through the main port defined in constructor method.
        :param user:
        :param password:
        :return:
        """
        self.user = user
        self.password = password

    def set_ssl_auth(self, pem_file: str=None, key_file: str=None, key_password: str=None):
        """
        Defines SSL credentials that must be used to communicate with this router instance
        through its main port.
        :param pem_file:
        :param key_file:
        :param key_password:
        :return:
        """
        self.pem_file = pem_file
        self.key_file = key_file
        # Set to None when empty as well
        self.key_password = None if not key_password else key_password

    def has_credentials(self) -> bool:
        return self.user and self.password

    def has_ssl_keys(self):
        return self.pem_file and self.key_file
