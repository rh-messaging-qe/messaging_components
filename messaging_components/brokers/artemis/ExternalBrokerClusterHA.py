import json
import logging
import pprint
import re

import time
from requests import ConnectionError

from messaging_components.brokers.artemis import Utils, ExternalBrokerOperableHA
from messaging_components.brokers.artemis.ExternalBrokerCluster import ExternalBrokerCluster

LOGGER = logging.getLogger(__name__)


class ClusterException(Exception):
    """Various Cluster exception"""
    pass


class RestoreInitialTopologyException(ClusterException):
    """Exception tied to restoring initial topology of deployed SUT models."""
    pass


class ExternalBrokerClusterHA(ExternalBrokerCluster):
    """This class represents a High Availability cluster of External Brokers defined with
    configuration input file.

    The primary broker here acts as the HA service which is active in communication
    with other clients.

    """
    # language=PythonRegExp
    topology_member_pattern = re.compile('TopologyMember.*]')
    """matching TopologyMember[.*] where master-slave pairs are defined"""

    # language=PythonRegExp
    pseudohost_pattern = re.compile('host=(.*?)[,\]&]')
    """matching IP addresses from host=(.*)"""

    def __init__(self, in_fopts, in_testcontainer=None, in_opts=None):
        super(ExternalBrokerClusterHA, self).__init__(in_fopts, in_testcontainer, in_opts)
        self.masters = []
        self.slaves = []
        self.pairs = set()
        self.default_broker = None

    def get_masters(self):
        """Return a list of all master brokers from this HA cluster service.

        :return: currently known master brokers in this HA cluster service
        :rtype: list[ExternalBrokerOperableHA]
        """
        return self.masters

    def get_slaves(self):
        """Return a list of all slave brokers from this HA cluster service.

        :return: currently known slave brokers in this HA cluster service
        :rtype: list[ExternalBrokerOperableHA]
        """
        return self.slaves

    def get_master_slave_pairs(self):
        """Return a list of pairs of master-slave brokers from this HA cluster service.

        :return: currently known master-slave broker pairs in this HA cluster service
        :rtype: list[(ExternalBrokerOperableHA, ExternalBrokerOperableHA)]
        """
        return self.pairs

    def reset_topology(self):
        """Reset currently known topology."""
        LOGGER.warn("Resetting current topology")
        self.masters = []
        self.slaves = []
        self.pairs = set()
        for broker in self.brokers:
            broker.reset_topology()

    def update_topology(self):
        """Figure out new topology, by contacting each of the brokers in (ha) cluster.
        This is done by doing Jolokia calls on Topology of the broker.
        """
        self.reset_topology()  # Forget previous topology. Find out actual.
        for broker in self.get_running_brokers():
            result = Utils.retry(funct=lambda: self._get_current_topology(broker),
                                 expected_result=None, max_count=10, max_duration=40,
                                 check_funct=lambda a, b: a is not None)
            current_topology = result[1]
            LOGGER.debug('broker: %s : %s\n' % (broker, pprint.pformat(current_topology)))
            if current_topology is None:
                LOGGER.warn("Unable to contact %s for topology update!" % broker)
                return

            self._set_pairs_from_topology_query(current_topology)
            self._set_default_broker()

    def _set_default_broker(self):
        """Set 'default' broker for this HA service - pick one of master brokers."""
        LOGGER.debug("Available brokers=%s" % [brk.get_data().get_instance_name() for brk in self.brokers])

        if self.default_broker is None and len(self.brokers) == 1:
            self.default_broker = self.brokers[0]
        else:
            for broker in self.get_masters():
                self.default_broker = broker
                break

        LOGGER.debug("Using default_broker=%s" % self.default_broker.get_data().get_instance_name())

    def add_external_broker(self, broker):
        """Append new broker to this cluster object instance.
        This is a mapping of broker_instance_name + broker.

        :param broker: to be added to this cluster representation
        :type broker: ExternalBrokerOperableHA
        """
        self.brokers.append(broker)
        if broker.get_ha_data().is_master():
            self.masters.append(broker)
        else:
            self.slaves.append(broker)

        self._set_default_broker()
        self.get_associated_nodes(broker)

    @staticmethod
    def wait_for_liveness(live_broker, backup_broker=None):
        """Wait until backup broker becomes live by connecting to broker.
        Use a connector client for this task and try to connect to default port.

        :param live_broker: broker which should become live soon
        :type live_broker: ExternalBrokerOperableHA
        :param backup_broker: broker which should become backup soon
        :type backup_broker: ExternalBrokerOperableHA
        """
        LOGGER.info("Wait for broker '%s' to become live." % live_broker)
        connector_cli_opts = {'obj-ctrl': 'C', live_broker.msg_processor.ADDRESS: None}

        Utils.retry(funct=lambda: live_broker.msg_processor.connect(connector_cli_opts, report=False),
                    max_count=15, max_duration=50, expected_result=True,
                    check_funct=lambda a, b: a.get_reported_connections_count() > 0)
        LOGGER.info("Connection to newly live-broker succeeded.")

        if backup_broker:
            Utils.retry(funct=lambda: backup_broker.msg_processor.connect(connector_cli_opts, report=False,
                                                                          expect_result=False),
                        max_count=15, max_duration=50, expected_result=True,
                        check_funct=lambda a, b: a.get_reported_not_opened_connections_count() > 0)
            LOGGER.info("Backup broker '%s' not accessible anymore." % backup_broker)
            LOGGER.debug("Waiting for few seconds for back-up to get topology update")
            time.sleep(5)

    def _get_topology_mapping_list(self, topology_response):
        """From jolokia topology response get IPs by using 2 regular expressions defined above in the class.
        Possible options are (<master>, <slave>), (<master>, None), (None, <slave>).
        The last one is tricky and is used, when 'topology_member_pattern' is not present in topology.

        :param topology_response: response from Topology of broker via Jolokia call
        :type topology_response: str
        :return: list of IP pairs
        :rtype: list
        """
        ip_list = []
        topology_member_list = self.topology_member_pattern.findall(topology_response)

        if topology_member_list:
            # master-slave pair found, make them a tuple and add them to ip_list
            for topology_pair in topology_member_list:
                pair = self.pseudohost_pattern.findall(topology_pair)
                # replace - by . in pseudo-ips list and make a tuple of [(master1, slave1)] pairs
                pair = [x.replace('-', '.') for x in pair]

                if len(pair) == 1:
                    pair.append(None)
                ip_list.append(tuple(pair))
        else:
            # topology member not present, most probably isolated slave
            # create (None, <slave>) tuple pair
            single_slave = self.pseudohost_pattern.findall(topology_response)
            pair = [x.replace('-', '.') for x in single_slave]
            pair.insert(0, None)
            ip_list.append(tuple(pair))
        return ip_list

    def _set_pairs_from_topology_query(self, topology_response):
        """Based on parsed data from topology response,
        this function sets master, slave broker, and sets HA pair accordingly.

        :param topology_response: response from Topology of broker via Jolokia call
        :type topology_response: str
        """
        ip_list = self._get_topology_mapping_list(topology_response)

        # ip_list example: [('10.37.145.203', '10.37.145.205'), (None, '10.37.145.214'), ('10.37.145.202', None)]
        broker_ip_mapping = {}
        master_broker = None
        slave_broker = None
        for broker in self.brokers:  # type: ExternalBrokerOperableHA
            broker_ssh_addr = broker.get_data().get_internal_address()
            broker_ip_mapping[broker_ssh_addr] = broker

        # Associate master, slave pairs and models together
        # according broker_ip_mapping and jolokia topology call
        for master_ip, slave_ip in ip_list:
            if master_ip is not None:
                broker_ip_mapping[master_ip].is_master = True
                if broker_ip_mapping[master_ip] in self.masters:
                    LOGGER.debug("Broker already in master list.")
                else:
                    LOGGER.debug("Adding broker to master list.")
                    self.masters.append(broker_ip_mapping[master_ip])
                master_broker = broker_ip_mapping[master_ip]

            if slave_ip is not None:
                broker_ip_mapping[slave_ip].master = False
                if broker_ip_mapping[slave_ip] in self.slaves:
                    LOGGER.debug("Broker already in slave list.")
                else:
                    LOGGER.debug("Adding broker to slave list.")
                    self.slaves.append(broker_ip_mapping[slave_ip])
                slave_broker = broker_ip_mapping[slave_ip]

            # Map cross-reference between master and slave broker
            if slave_ip is not None and master_ip is not None:
                broker_ip_mapping[master_ip].slave_broker = broker_ip_mapping[slave_ip]
                broker_ip_mapping[slave_ip].master_broker = broker_ip_mapping[master_ip]

            self.pairs.add((master_broker, slave_broker))

    def _get_current_topology(self, broker):
        """Get a list of associated broker nodes for this broker object from jolokia call.
        See ExternalBroker.get_associated_nodes() for details about format.

        http://<node>:8161/console/jolokia/read/org.apache.activemq.artemis:broker="amq-10-37-145-204",
        component=cluster-connections,name=%22my-cluster%22/Nodes or /Topology
        :param broker: execute jolokia call on this object
        :type broker: ExternalBrokerOperable
        :return: mapping of internal brokerIDs and hosts in cluster or None, if we did not manage to get it
        :rtype: str or None
        """
        cluster_nodes_template_dict = {'HOST': broker.get_data().get_ssh_address(),
                                       'PORT': broker.get_data().get_ports().get('web'),
                                       'QUERY_OPERATION': 'read',
                                       'BROKER_NAME': broker.get_data().get_instance_name(),
                                       'OPERATION': ',component=cluster-connections,name="%s"/Topology'
                                                    % self.get_cluster_group_name()
                                       }
        ha_topology = None
        try:
            response_data = broker.do_read_request(cluster_nodes_template_dict)
            LOGGER.debug("response_text=%s" % response_data.text)
            ha_topology = json.loads(response_data.text).get('value')

        except ConnectionError as ce:
            LOGGER.debug("Unable to connect to broker on %s. %s" % (broker.get_data().get_ssh_address(), ce))
        return ha_topology

    def do_check_initial_topology_preserved(self, tcg_initial_topology):
        """Perform check if initial topology is preserved after test finished.
        If not, call routine to restart all brokers and set initial topology again.
        """
        preserved = self.test.add_check_and_report(in_desc="Initial topology is preserved",
                                                   in_result_exp=tcg_initial_topology,
                                                   in_result=self.get_master_slave_pairs())
        if not preserved:
            tcg_initial_topology = self.do_restore_initial_topology()
        return preserved

    def do_restore_initial_topology(self):
        """Routine to kill & restart all brokers in HA service.
        Called only when check initial topology fails or original topology to be reverted back.

        :return: whether were all brokers successfully started again
        :rtype: bool
        """
        for broker in self.brokers:
            accessible = broker.is_accessible()
            if not accessible:
                self.test.add_error(in_desc='Broker %s is unexpectedly unaccessible!' % broker)

        LOGGER.warn("Current topology=%s", self.get_master_slave_pairs())
        LOGGER.warn("At least one broker is unexpectedly unaccessible, performing kill9-restart routine!")
        brokers_started = []
        for broker in self.brokers:
            broker.stop(in_killsig_id=9)

        for broker in self.brokers:
            brokers_started.append(broker.start(wait_for_accessible=True))

        self.update_topology()

        if all(brokers_started):
            return self.get_master_slave_pairs()
        else:
            raise RestoreInitialTopologyException("Unable to restore Initial Topology! Exitting whole execution!")
            # dtestlib.test.AbortTest()/TCG
            exit(5)  # TODO mtoth: need help from zkraus to handle this better
            # return False

    # ==== Debugging methods ====

    def update_topology(self):
        """Figure out new topology, by contacting each of the brokers in (ha) cluster.
        This is done by doing Jolokia calls on Topology of the broker.
        """
        self.reset_topology()  # Forget previous topology. Find out actual.
        for broker in self.get_running_brokers():
            result = Utils.retry(funct=lambda: self._get_current_topology(broker),
                                 expected_result=None, max_count=10, max_duration=40,
                                 check_funct=lambda a, b: a is not None)
            current_topology = result[1]
            LOGGER.debug('broker: %s : %s\n' % (broker, pprint.pformat(current_topology)))
            if current_topology is None:
                LOGGER.warn("Unable to contact %s for topology update!" % broker)
                return

            self._set_pairs_from_topology_query(current_topology)
            self._set_default_broker()

    def do_print_masters(self):
        """Print information about master and their respective slave brokers in HA topology.

        :param ha_service: messaging HA service container to get master & slave brokers from
        :type ha_service: ExternalBrokerClusterHA
        """
        for master in self.get_masters():
            if master.slave_broker:
                slave_instance_name = master.slave_broker.get_data().get_instance_name()
            else:
                slave_instance_name = None
            LOGGER.info("master:%s, instance:%s, slave:%s", master.get_data().get_instance_name(),
                        master.get_data().get_instance_home_dir(),
                        slave_instance_name)

    def do_print_slaves(self):
        """Print information about slaves and their master brokers in HA topology.

        :param ha_service: messaging HA service container to get master & slave brokers from
        :type ha_service: ExternalBrokerClusterHA
        """
        for slave in self.get_slaves():  # type: ExternalBrokerOperableHA
            master_broker_instance_name = None
            if slave.master_broker:
                master_broker_instance_name = slave.master_broker.get_data().get_instance_name()

            LOGGER.info("slave:%s, instance:%s, master:%s", slave.get_data().get_instance_name(),
                        slave.get_data().get_instance_home_dir(),
                        master_broker_instance_name)
