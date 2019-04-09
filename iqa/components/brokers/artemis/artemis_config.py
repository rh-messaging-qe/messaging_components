import logging
import posixpath

from amqcfg import amqcfg

from iqa.abstract.components.component import Component
from iqa.abstract.messaging.user import User
from iqa.components.brokers.broker_config import BrokerConfiguration
from iqa.components.config.config import Utils, IQAConfigurationException


class ArtemisConfig(BrokerConfiguration):
    """Placeholder class of read configuration details for Artemis/AMQ 7
    from provided input file.
    Input file is json supported only (yaml in the future).

    This class is directly tied to ExternalBroker.
    """
    DEFAULT_HOME = "/opt/jboss-amq-7"
    DEFAULT_INSTANCE_HOME = "/opt/jboss-amq-7-i0"
    DEFAULT_INSTANCE_NAME = "amq"
    DEFAULT_USERS = {
        "admin": {
            "password": "admin",
            "role": "amq",
            "key": "/path/to/key",
            "ticket": "/path/to/ticket"
        },
        "tckuser": {
            "password": "tckuser",
            "role": "amq"
        },
        "superuser": {
            "password": "superuser",
            "role": "amq"
        },
        "administrator": {
            "password": "administrator",
            "role": "amq"
        },
        "nobody": {
            "password": "nobody",
            "role": "amq"
        }
    }
    DEFAULT_PORTS = {
        "openwire": 61616,
        "amqp": 5672,
        "mqtt": 1883,
        "core": 5445,
        "stomp": 61613,
        "web": 8161,
        "jmx": 1099
    }
    DEFAULT_PORT_JMX = 1099
    DEFAULT_PORT_WEB = 8161

    P_PROFILE_PATH = "render/profile_path"
    P_HOME = "artemis_profile/home"
    P_INSTANCE_NAME = "broker_xml/name"
    P_INSTANCE_HOME = "artemis_profile/instance"
    P_INSTANCE_DIR_ETC = "artemis_profile/instance_etc_uri"
    P_INSTANCE_DIR_DATA = "artemis_profile/data_dir"

    P_USERS = "artemis_users"
    P_ROLES = "artemis_roles"

    P_PORTS = "broker_xml/acceptors"
    P_WEB_PORT = "bootstrap_xml/web/bind/port"
    P_JMX_PORT = "management_xml/connector_port"

    instance_name = None
    instance_home = None
    instance_home_etc = None
    instance_home_data = None
    instance_home_log = None
    instance_home_tmp = None

    home = None
    amqcfg_profile_path = None

    def __init__(self, component: Component, **kwargs):
        """Initialize ExternalBrokerData from provided configuration file.

        :param broker_data: empty data object, to be filled with provided configuration data
        :type broker_data: ExternalBrokerData
        :param test_node: test node which is running given broker
        :type test_node: TestNode
        """
        super(ArtemisConfig, self).__init__(component, **kwargs)
        self.node_config_dir = self.instance_home_etc

    def create_default_configuration(self, **kwargs):
        self.home = kwargs.get('broker_home', self.DEFAULT_HOME)
        self.instance_home = kwargs.get('broker_path', self.DEFAULT_INSTANCE_HOME)
        self.instance_name = kwargs.get('broker_name', self.DEFAULT_INSTANCE_NAME)
        self.ports['web'] = kwargs.get('broker_web_port', self.DEFAULT_PORT_WEB)
        self.users['admin'] = User('admin', 'admin', roles=['amq'])

    def create_configuration(self, config_file_path):
        self.load_configuration_yaml(config_file_path)
        self.load_configuration()

    def load_configuration(self):
        self.home = self._data_getter(self.P_HOME, self.DEFAULT_HOME)
        self.instance_home = self._data_getter(self.P_INSTANCE_HOME, self.DEFAULT_INSTANCE_HOME)
        self.instance_name = self._data_getter(self.P_INSTANCE_NAME, self.DEFAULT_INSTANCE_NAME)
        self.instance_home_etc = Utils.remove_prefix(self._data_getter(self.P_INSTANCE_DIR_ETC), "file:")
        self.instance_home_data = self._data_getter(self.P_INSTANCE_DIR_DATA)
        self.instance_home_log = posixpath.join(self.instance_home, "log")
        self.instance_home_tmp = posixpath.join(self.instance_home, "tmp")
        self.ports = self.assign_ports()
        self.assign_users()
        self.amqcfg_profile_path = self._data_getter(self.P_PROFILE_PATH)
        # self.topology = TopologyData(broker_data) or None

    def assign_ports(self):
        ports = {}
        acceptors = self._data_getter(self.P_PORTS, self.DEFAULT_PORTS)

        for acceptor in acceptors:
            ports[acceptor.get('name')] = acceptor.get('port')

        ports['jmx'] = self._data_getter(self.P_JMX_PORT, self.DEFAULT_PORT_JMX)
        ports['web'] = self._data_getter(self.P_WEB_PORT, self.DEFAULT_PORT_WEB)
        return ports

    def assign_users(self):
        """
        :return:
        :rtype:
        """
        tmp_users = self._data_getter(self.P_USERS, self.DEFAULT_USERS)
        roles = self._data_getter(self.P_ROLES)

        for user in tmp_users:
            self.users[user] = (User(user, tmp_users[user]))

        for role in roles.keys():
            for user_in_role in roles[role]:
                user_obj = self._get_user(user_in_role)
                user_obj.roles.append(role)

    def get_users(self):
        return self.users

    def get_acceptors(self):
        return self.ports

    def _get_user(self, username):
        return self.users.get(username)

    def get_username(self, user):
        return self._get_user(user).username

    def get_user_password(self, user):
        return self._get_user(user).password

    def apply_config(self, yaml_configuration_path, restart=True):
        # self.store_configuration()
        try:
            # Todo hacky way to turn off debug logging from amqcfg module
            amqcfg.LOG.setLevel(logging.WARN)
            if self.LOGGER.level != logging.DEBUG:
                amqcfg.LOG.setLevel(logging.WARN)
            amqcfg.generate(profile=yaml_configuration_path,
                            output_path=self.local_config_dir,
                            write_profile_data=True)
            exec = self.copy_configuration_files()

            if exec.completed_successfully():
                self.load_configuration_yaml(yaml_configuration_path)
                self.load_configuration()
            else:
                self.LOGGER.error(exec.read_stderr())
                raise IQAConfigurationException("Unable to copy config files to node.")
        except Exception:
            self.restore_config()
            raise IQAConfigurationException("Unable to apply new configuration. Original config kept.")
        finally:
            self.LOGGER.info("Configuration from '%s' successfully applied." % yaml_configuration_path)

        if restart and self.component.service is not None:
            self.component.service.restart(wait_for_messaging=True)
