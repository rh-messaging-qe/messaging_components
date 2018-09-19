import json
import logging

from requests import ConnectionError

from messaging_components.brokers.artemis import ExternalBrokerClusterHA
from messaging_components.brokers.artemis.AbstractExternal import AbstractExternal

LOGGER = logging.getLogger(__name__)


class ExternalBrokerCluster(AbstractExternal):
    """This class represents a cluster of External Brokers defined with
    configuration input file.

    The primary broker here acts as the one which is active in communication
    with other clients.

    """
    brokers = []
    default_broker = None

    def _set_default_broker(self):
        """Set given instance name broker as primary
        or get first found broker (by python key) by default.
        """
        LOGGER.debug("Available brokers=%s" % [brk.get_data().get_instance_name() for brk in self.brokers])

        if self.default_broker is None and len(self.brokers) == 1:
            self.default_broker = self.brokers[0]
        else:
            for broker in self.get_running_brokers():
                self.default_broker = broker
                break

        LOGGER.debug("Using default_broker=%s" % self.default_broker.get_data().get_instance_name())

    def get_default_broker(self):
        """Return default broker (first active).
        :return: currently used "default" broker object
        :rtype: ExternalBroker
        """
        return self.default_broker

    def get_urls(self, in_preferred_only_ena=False, in_update_ena=False, in_credentials_ena=None):
        """Return ip address/hostname of node for this broker.

        All parameters are used only for backwards compatibility of inheritance!
        :param in_preferred_only_ena: preferred ports
        :type in_preferred_only_ena: bool
        :param in_update_ena: update enable
        :type in_update_ena: bool
        :param in_credentials_ena: use credentials
        :type in_credentials_ena: bool
        :return: IP address/hostname provided in "default_address" of configuration file
        :rtype: str
        """
        return self.default_broker.get_urls(in_preferred_only_ena=False, in_update_ena=False, in_credentials_ena=None)

    def get_annotated_ports(self, in_update_ena=False):
        """Return a mapping of port and running services on External service.

        :param in_update_ena: not used (only for inheritance backwards compatibility here)
        :type in_update_ena: bool
        :return: mapping for service type : port for External service
        :rtype: dict
        """
        return self.default_broker.get_annotated_ports(in_update_ena)

    def add_external_broker(self, broker):
        """Append new broker to this cluster object instance.
        This is a mapping of broker_instance_name + broker.

        :param broker: to be added to this cluster representation
        :type broker: ExternalBroker
        """
        self.brokers.append(broker)
        self._set_default_broker()
        self.get_associated_nodes(broker)

    def kill(self, signal, broker):
        """Kill given broker with defined signal.
        :param signal: linux signal to be used for kill command
        :type signal: int
        :param broker: which broker to kill/stop
        :type broker: ExternalBrokerOperable
        """
        broker.stop(in_killsig_id=signal)
        broker.set_running(False)
        self._set_default_broker()

    def get_running_brokers(self):
        """Return a list of running brokers (having a PID number).
        :return: broker objects which are running
        :rtype: list[ExternalBrokerOperable]
        """
        return [broker for broker in self.get_brokers() if broker.is_running()]

    def get_brokers(self):
        """Return broker objects in this cluster service.
        :return: list of broker objects in cluster
        :rtype: list [ExternalBrokerOperable]
        """
        return self.brokers

    def get_state(self, in_update_ena=False):
        """Return state of the broker - assume all is OK for now - External service.

        :param in_update_ena: Method not used, just because of backwards compatibility.
        :type in_update_ena: bool
        :return: Assume everything is ok with broker objects
        :rtype: bool
        """
        return True

    def get_cluster_group_name(self):
        """Return name of the cluster group.
        :return: name of the cluster group of this cluster object
        :rtype: str
        """
        cluster_name = self.default_broker.get_data().get_cluster_data().get_connection_data().get_name()
        return cluster_name

    def get_associated_nodes(self, broker):
        """Get a list of associated broker nodes for this broker object from jolokia call.
        See ExternalBroker.get_associated_nodes() for details about format.

        http://${HOST}:${PORT}/console/jolokia/${QUERY_OPERATION}/
        org.apache.activemq.artemis:broker="${BROKER_NAME}"${OPERATION}

        :param broker: execute jolokia call on this object
        :type broker: ExternalBrokerOperable
        :return: mapping of internal brokerIDs and hosts in cluster
        :rtype: dict
        """
        cluster_nodes_template_dict = {'HOST': broker.get_data().get_ssh_address(),
                                       'PORT': broker.get_data().get_ports().get('web'),
                                       'QUERY_OPERATION': 'read',
                                       'BROKER_NAME': broker.get_data().get_instance_name(),
                                       'OPERATION': ',component=cluster-connections,name="%s"/Nodes'
                                                    % self.get_cluster_group_name()
                                       }
        try:
            response_data = broker.do_read_request(cluster_nodes_template_dict)
            LOGGER.debug("response_text=%s" % response_data.text)
            cluster_nodes = json.loads(response_data.text).get('value')
            broker.set_associated_nodes(cluster_nodes)

        except ConnectionError as ce:
            LOGGER.debug("Unable to connect to broker on %s. %s" % (broker.get_data().get_ssh_address(), ce))
            cluster_nodes = {}
        return cluster_nodes

    def reset_topology(self):
        pass

    def update_topology(self):
        pass

    # ===== Internal helper methods =====
    def do_update_topology_and_print(self):
        """Update topology to reflect new status.
        Print information about masters, slaves and running brokers.

        """
        self.update_topology()
        self.do_print_running_brokers()

        if isinstance(self, ExternalBrokerClusterHA.ExternalBrokerClusterHA):
            self.do_print_masters()
            self.do_print_slaves()

    def do_print_running_brokers(self):
        """Print information about all currently running brokers
        in cluster or HA topology.
        """
        msg_data = ""
        for brk in self.get_running_brokers():
            msg_data += "\n%s pid:%s" % (brk.get_data().get_instance_name(), brk.get_pid())
        LOGGER.info("Running brokers: %s", msg_data)