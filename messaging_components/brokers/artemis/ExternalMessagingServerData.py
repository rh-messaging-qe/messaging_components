import json
import posixpath
import dpath
from abc import abstractmethod

import yaml
import logging


LOGGER = logging.getLogger(__name__)

class ExternalMessagingServerData(yaml.YAMLObject):
    """Placeholder class of read configuration details from provided input file.
    Input file is json supported only (yaml in the future).
    """
    data_dict = None
    object_list = []

    def super_getter(self, path, default=None):
        """

        :param path:
        :type path:
        :param default:
        :type default:
        :return:
        :rtype:
        """
        output = None
        try:
            output = dpath.get(self.data_dict, path)
        except (KeyError, ValueError) as exc:
            LOGGER.debug('Unknown key or value %s', path)
            return default
        return output

    def _set_id(self, id):
        self.server_id = id

    def get_objects_count(self):
        return len(self.object_list)

    def load_configuration_yaml(self, path):
        """Load provided configuration YAML file.

        :param path: path to configuration file
        :type path: str
        :return: List of initialized messaging servers (as objects)
        :rtype: list
        """
        if self.object_list == []:
            with open(path, 'r') as f:
                settings_yaml = yaml.load(f, Loader=yaml.Loader)
                for key in settings_yaml.keys():
                    templatename = settings_yaml[key]['render']['template']

                    if "artemis" in templatename:
                        self.object_list.append(ExternalBrokerData(settings_yaml[key]))
                    elif "interconnect" in templatename:
                        self.object_list.append(ExternalMessagingServerData(settings_yaml[key]))
                    else:
                        raise KeyError("Unknown ExternalData type!" + settings_yaml[key])
        return self.object_list

    # === Custom decoder object for JSON
    @staticmethod
    def object_decoder(obj):
        """Map configuration from json to External* object models.

        :param obj: provided json object
        :type obj: dict
        :return: decoded json object
        :rtype: ExternalMessagingServerData (child)
        """
        if 'type' in obj and obj['type'] == 'ArtemisBroker':
            return ExternalBrokerData(obj['broker'], obj['node_information'])

        if 'type' in obj and obj['type'] == 'Interconnect':
            return ExternalInterconnectData()
        return obj

    def load_configuration_json(self, path):
        """Load provided configuration JSON file.

        :param path: path to configuration file
        :type path: str
        :return: List of initialized messaging servers (as objects)
        :rtype: list
        """
        # --- Method 1 - quick but access to object is sad
        # ext = json.loads(open(path).read(), object_hook=lambda d: Namespace(**d))
        # print type(ext)
        # print ext.amq0
        # print ext.amq0.broker
        # print ext.amq0.type

        # --- Method 2 - nice object creation a bit harder
        settings_json = json.loads(open(path).read())
        object_list = []
        for key in settings_json:
            server = json.loads(json.dumps(settings_json[key]), object_hook=self.object_decoder)
            server._set_id(key)
            object_list.append(server)

        return object_list

    @abstractmethod
    def get_ssh_address(self):
        """Return default address for connection

        :return: IP of hostname provided in configuration
        :rtype: str
        """
        pass

    @abstractmethod
    def get_ports(self):
        """Get dictionary of mapping protocol:number

        :return: mapping of protocol:number
        :rtype: dict
        """
        pass


class ExternalInterconnectData(ExternalMessagingServerData):
    def get_ssh_address(self):
        """Return default address for connection

        :return: IP of hostname provided in configuration
        :rtype: str
        """
        pass

    def get_ports(self):
        """Get dictionary of mapping protocol:number

        :return: mapping of protocol:number
        :rtype: dict
        """
        pass

    def get_default_address(self):
        """Get default address to broker (or test node)

        :return: provided configuration default_address
        :rtype: address
        """
        pass


class ExternalBrokerData(ExternalMessagingServerData):
    """Placeholder class of read configuration details for Artemis/AMQ 7
    from provided input file.
    Input file is json supported only (yaml in the future).

    This class is directly tied to ExternalBroker.
    """
    DEFAULT_HOME = "/opt/jboss-amq-7"
    DEFAULT_HOME_INSTANCE = "/opt/jboss-amq-7-i0"
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

    P_HOME = "artemis_profile/home"
    P_NODE_INFO = "node_information"
    P_INSTANCE_HOME = "artemis_profile/instance"

    P_INSTANCE_NAME = "broker_xml/name"
    P_DATA_DIR = "artemis_profile/data_dir"
    P_USERS = "artemis_users"
    P_ROLES = "artemis_roles"
    P_PORTS = "broker_xml/acceptors"

    P_WEB_PORT = "bootstrap_xml/web/bind"
    P_JMX_PORT = "management_xml/connector_port"

    def __init__(self, broker_data, test_node=None):
        """Initialize ExternalBrokerData from provided configuration file.

        :param broker_data: empty data object, to be filled with provided configuration data
        :type broker_data: ExternalBrokerData
        :param test_node: test node which is running given broker
        :type test_node: TestNode
        """
        # TODO
        self.data_dict = broker_data
        self.home = self.super_getter(self.P_HOME, self.DEFAULT_HOME)

        self.instance_home = self.super_getter(self.P_INSTANCE_HOME, self.DEFAULT_HOME_INSTANCE)
        self.instance_name = self.super_getter(self.P_INSTANCE_NAME, self.DEFAULT_INSTANCE_NAME)

        self.ports = self.assign_ports()
        self.users = self.assign_users()

        self.topology = TopologyData(broker_data) or None
        self.node_information = self.super_getter(self.P_NODE_INFO, test_node)
        self.test_node = test_node

    def _set_id(self, id):
        """Set id for this broker.

        :param id: ID provided from config file
        :type id: str
        """
        self.server_id = id

    def get_id(self):
        """Get broker ID from provided configuration file.

        :return: ID for this broker from configuration file
        :rtype: str
        """
        return self.server_id

    def __str__(self):
        """Print part of state of this object/instance.

        :return: string representation of this object.
        :rtype: str
        """
        return "server_id=%s\n" \
               "home=%s\n" \
               "instance_home=%s\n" \
               "ports=%s\n" \
               "default_addr=%s\n" \
               "node=%s\n)" % (
                   self.server_id, self.home, self.instance_name, self.ports, self.get_default_address(),
                   self.test_node)

    def assign_ports(self):
        """
        :return:
        :rtype:
        """
        ports = {}
        acceptors = self.super_getter(self.P_PORTS)

        for acceptor in acceptors:
            ports[acceptor['name']] = acceptor['port']

        ports['jmx'] = self.super_getter(self.P_JMX_PORT, self.DEFAULT_PORT_JMX)
        # todo(mtoth) temporary workaround
        ports['web'] = self.DEFAULT_PORT_WEB
        # web_port = self.super_getter(self.P_JMX_PORT, self.DEFAULT_PORT_WEB)
        return ports

    def assign_users(self):
        """
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
        :return:
        :rtype:
        """
        users = []
        tmp_users = self.super_getter(self.P_USERS, self.DEFAULT_USERS)
        roles = self.super_getter(self.P_ROLES)

        for user in tmp_users:
            users.append(User(user, tmp_users[user]))


        for role in roles.keys():
            for user_in_role in roles[role]:
                # users[user]['roles'].append(role)
                for user in users:
                    if user.username == user_in_role:
                        user.add_role(role)
                        break
        return users

    def get_home_dir(self):
        """Get broker home directory (not instance).

        :return: path to home directory of broker
        :rtype: str
        """
        return self.home

    def get_instance_home_dir(self):
        """Get broker instance directory.

        :return: path to instance directory of broker
        :rtype: str
        """
        return self.instance_home

    def get_instance_conf_dir(self):
        """Get broker instance conf directory (<instance>/etc).

        :return: path to instance/etc directory of broker
        :rtype: str
        """
        # TODO(mtoth) might be movable
        return posixpath.join(self.instance_home, 'etc')

    def get_instance_bin_dir(self):
        """Get broker instance binary directory (<instance>/bin).

        :return: path to instance/bin directory of broker
        :rtype: str
        """
        return posixpath.join(self.instance_home, 'bin')

    def get_instance_log_dir(self):
        """Get broker instance log directory (<instance>/log).

        :return: path to instance/log directory of broker
        :rtype: str
        """
        return posixpath.join(self.instance_home, 'log')

    def get_instance_data_dir(self):
        """Get broker instance data directory (<instance>/data).

        :return: path to instance/data directory of broker
        :rtype: str
        """
        # TODO(mtoth) might be movable
        return posixpath.join(self.instance_home, 'data')

    def get_instance_name(self):
        """Get broker instance name from provided configuration

        :return: broker instance name
        :rtype: str
        """
        return self.instance_name

    def get_ssh_address(self):
        """Return default address for connection

        :return: IP of hostname provided in configuration
        :rtype: str
        """
        # TODO(mtoth) return self.node_information.get_opt('node')
        return self.get_default_address()

    def get_default_address(self):
        """Get default address to broker (or test node)

        :return: provided configuration default_address
        :rtype: address
        """
        try:
            address = self.node_information.get('default_address')
        except AttributeError:
            address = self.node_information.get_opt('node')
        return address

    def get_internal_address(self):
        """Get internal address to broker (or test node).
        Ideal when used in Openstack environment, where internal IPs are different than
        publicly available outside of Openstack.

        :return: provided configuration default_address
        :rtype: address
        """
        try:
            address = self.node_information.get('addresses').get('internal')
            if address is None:
                address = self.node_information.get('addresses').get('default_ssh')
        except AttributeError:
            address = self.node_information.get_opt('node')
        return address

    def get_test_node(self):
        """Get test node for this broker data object from provided configuration.

        :return: associated test node of this broker
        :rtype: TestNode
        """
        return self.test_node

    def set_test_node(self, test_node):
        """Set test node for this broker from provided configuration.

        :param test_node: associated test node of this broker
        :type test_node: TestNode
        """
        self.test_node = test_node

    def get_ports(self):
        """Get dictionary of mapping protocol:number

        :return: mapping of protocol:number
        :rtype: dict
        """
        return self.ports

    def get_users(self):
        """Get users from provided configuration

        :return: dict of users with details about these users
        :rtype: dict
        """
        return self.users

    def get_admin_user(self):
        """Get admin user for this broker

        :return: admin user for this broker
        :rtype: str
        """
        for user in self.users:
            if "amq" in user.roles:
                return user

    def get_admin_password(self):
        """Get admin user password for this broker

        :return: admin user password for this broker
        :rtype: str
        """
        return 'admin'
        return self.get_admin_user().password

    def get_users_plain_dtests_format(self):
        """Get users in dtests plain format

        :return: users with username & password
        :rtype: dict
        """
        users = {}
        # for user in self.users:
        #     users['username'] = user
        #     users['password'] = self.users[user].get('password')
        #     # TODO hack to return only first user!!
        users['username'] = self.get_admin_user().username
        users['password'] = self.get_admin_password()

        return users

    def get_topology(self):
        """Get topology for this broker (cluster + ha data)

        :return: topology data provided from configuration file
        :rtype: TopologyData
        """
        return self.topology

    def get_broadcast_data(self):
        """Get broadcast part of topology data provided from configuration file.

        :return: Cluster broadcast data for this broker
        :rtype: BroadcastData
        """
        return self.topology.get_broadcast_data()

    def get_cluster_data(self):
        """Get cluster data part of topology data provided from configuration file.

        :return: Cluster connection data for this broker
        :rtype: ClusterConnectionData
        """
        return self.topology.get_cluster_data()

    def get_discovery_data(self):
        """Get cluster discovery data part of topology data provided from configuration file.

        :return: Cluster discovery data for this broker
        :rtype: DiscoveryData
        """
        return self.topology.get_discovery_data()

    def get_ha_data(self):
        """Get High Availability data part of topology data provided from configuration file.

        :return: HA data for this broker
        :rtype: HAData
        """
        return self.topology.get_ha_data()

class TopologyData(ExternalMessagingServerData):
    """Topology data representation object from provided configuration file. """

    P_CLUSTER = "broker_xml/cluster"
    P_CLUSTER_CONNS = "broker_xml/cluster_connections"
    P_BROADCAST = "broker_xml/broadcast_groups"
    P_DISCOVERY = "broker_xml/discovery_groups"
    P_HA_POLICY = "broker_xml/ha_policy"  # TODO untested

    def __init__(self, broker_data):
        """Initialize topology data from provided configuration file

        :param broker_data: topology part from configuration file
        :type broker_data: dict
        """
        self.data_dict = broker_data
        self.broadcast_data = BroadcastData(self.super_getter(self.P_BROADCAST, None))
        cluster_connection = self.super_getter(self.P_CLUSTER_CONNS, None)

        self.cluster_data = None
        if cluster_connection is not None:
            if not isinstance(cluster_connection, list):
                self.cluster_data = ClusterConnectionData(enumerate(cluster_connection))
            else:
                self.cluster_data = ClusterConnectionData(cluster_connection)

        self.discovery_data = DiscoveryData(self.super_getter(self.P_DISCOVERY, None))

        self.ha_data = None
        if self.super_getter(self.P_HA_POLICY, None):
            self.ha_data = HAData(self.super_getter(self.P_HA_POLICY))


    def get_topology_data(self):
        """Get whole topology data

        :return: topology data from configuration file
        :rtype: dict
        """
        return self.topology

    def get_broadcast_data(self):
        """Get broadcast data

        :return: broadcast data from configuration file
        :rtype: BroadcastData
        """
        return self.broadcast_data

    def get_cluster_data(self):
        """Get cluster connection data

        :return: cluster data from configuration file
        :rtype: ClusterConnectionData
        """
        return self.cluster_data

    def get_discovery_data(self):
        """Get discovery connection data

        :return: discovery data from configuration file
        :rtype: DiscoveryData
        """
        return self.discovery_data

    def get_ha_data(self):
        """Get HA connection data

        :return: HA data from configuration file
        :rtype: HAData
        """
        return self.ha_data


class ClusterConnectionData(ExternalMessagingServerData):
    connections = []

    def __init__(self, cluster_data):
        """Initialize cluster connections data from provided file

        :param cluster_data: data from provided file
        :type cluster_data: dict
        """
        if cluster_data is not None:
            for connection in cluster_data:
                self.connections.append(Connection(connection))
        else:
            self.cluster_data = None

    def get_connection_data_all(self):
        """Get all connections in this cluster

        :return: all Connection for this instance
        :rtype: list of Connection
        """
        return self.connections

    def get_connection_data(self):
        """Get first connection data of this cluster

        :return: first Connection for this instance
        :rtype: Connection
        """
        return self.connections[0]


class Connection(ExternalMessagingServerData):
    """Cluster connection representation."""

    def __init__(self, connection_data):
        """Initialize connection data from provided configuration file

        :param connection_data: part provided from file
        :type connection_data: dict
        """
        super(Connection, self).__init__()
        self.name = connection_data.get('name')
        self.connector_ref = connection_data.get('connector-ref')
        self.message_load_balancing = connection_data.get('message-load-balancing')
        self.max_hops = connection_data.get('max-hops')
        self.discovery_group_ref = connection_data.get('discovery-group-ref')

    def get_name(self):
        return self.name


class BroadcastData(object):

    def __init__(self, broadcast_data):
        pass


class DiscoveryData(object):

    def __init__(self, discovery_data):
        pass


class HAData(ExternalMessagingServerData):
    """High Availability representation of provided data for broker."""
    def __init__(self, ha_data):
        """Initialize ha data from provided configuration file

        :param ha_data: part provided from file
        :type ha_data: dict
        """
        self.ha_policies = []
        for ha_policy in ha_data:
            self.type = ha_policy.get('policy')
            self.master = ha_policy.get('role')
            self.properties = ha_policy.get('properties')
            # TODO(mtoth) more policies example?
            # self.failback_policy = ha_data.get('failback-policy')
            # self.check_for_live_server = ha_data.get('properties').get('check-for-live-server')
            # self.shared_store_location = ha_data.get('properties').get('shared-store-location')

    def is_master(self):
        """Return bool if master tag has been specified to True or False
        in provided configuration file.

        :return: provided True/False value in configuration file of master tag
        :rtype: bool
        """
        return self.master

class User(object):



    def __init__(self, username, password, *args, **kwargs):
        self._username = username
        self._password = password
        self._roles = set()

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def roles(self):
        return self._roles

    def add_role(self, role):
        self._roles.add(role)