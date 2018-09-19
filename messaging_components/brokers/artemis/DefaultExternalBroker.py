import logging

from messaging_components.brokers.artemis.AbstractExternal import AbstractExternal

LOGGER = logging.getLogger(__name__)

class DefaultExternalBroker(AbstractExternal):

    data = None
    test_node = None

    def __init__(self, in_fopts, in_testcontainer=None, in_opts=None):
        super(DefaultExternalBroker, self).__init__(in_fopts, in_testcontainer, in_opts)

    def start(self, in_exp_result=True):
        """Start external service.

        Might not be implemented for "external services".

        :param in_exp_result: expected result of this function
        :type in_exp_result: bool
        :return: success of starting given service
        :rtype: bool
        """
        pass

    def stop(self, in_killsig_id=0, in_stop_all_brokers_on_node=False):
        """Stop external service.

        Might not be implemented for "external services".

        :param in_killsig_id: killing signal to "kill" command
        :type in_killsig_id: int or str
        :param in_stop_all_brokers_on_node: whether to stop all servers on node
        :type in_stop_all_brokers_on_node: bool
        :return: success of stopping given service
        :rtype: bool
        """
        pass

    def cfg_apply(self):
        """Apply new configuration to External service.

        Not applicable for majority of External services

        :return: success of applying new configuration to External service
        :rtype: bool
        """
        pass

    def cfg_apply_dynamic(self):
        """Apply new configuration to External service without any restart to service (reload config).

        Not applicable for majority of External services

        :return: success of applying new configuration to External service
        :rtype: bool
        """
        pass

    def cfg_revert(self, in_exp_result=True):
        """Apply original/previous configuration to External service.

        Not applicable for majority of External services

        :return: success of applying original/previous configuration to External service
        :rtype: bool
        """
        pass

    def cfg_status(self):
        """Status of applying configuration.

        Not applicable for majority of External services

        :return: configuration status of External service
        :rtype: bool
        """
        return True

    def get_pid(self, in_update_ena=False):
        # we are not allowed to restart broker so we don't care about PID
        """Return current PID of external service

        Might not be implemented for "external services".

        :return: PID number of running service
        :rtype: int
        """
        return 1

    def get_port(self, in_type='amqp'):
        """Return port number of given service type of External service.

        Might not be implemented for "external services".

        :param in_type: Type of service running on External service
        :type in_type: str
        :return: port number of service running on External service
        :rtype: int
        """
        return self.get_annotated_ports().get(in_type)

    def get_ports(self, in_preferred_only_ena=False, in_update_ena=False):
        """Get ports for this broker (SUT model)

        :param in_preferred_only_ena: returns 'main' port
        :type in_preferred_only_ena: bool
        :param in_update_ena: force broker state update - INVALID
        :type in_update_ena: bool
        :return: list of selected ports
        :rtype: list[int]
        """
        if in_preferred_only_ena:
            return [self.get_annotated_ports().get(None)]

        return list(set(self.get_annotated_ports()))  # to keep this only in one place

    def set_test_node(self, test_node):
        """Set test node object to this broker instance.

        :param test_node: test node running external broker
        :type test_node: TestNode
        """
        self.test_node = test_node

    def get_test_node(self):
        """Get test node for this broker

        :return test_node: test node running external broker
        :rtype test_node: TestNode
        """
        return self.test_node

    def get_annotated_ports(self, in_update_ena=False):
        """Return a mapping of port and running services on External service.

        :param in_update_ena: not used (only for inheritance backwards compatibility here)
        :type in_update_ena: bool
        :return: mapping for service type : port for External service
        :rtype: dict
        """
        return {None: 5672, 'amqp': 5672, 'openwire': 61616, 'jmx-rmi': 1099}

    def get_annotated_dirs(self, in_update_ena=False):
        # TODO from current set of directories instance home and others, for getting logs and such
        return {}

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
        return super(DefaultExternalBroker, self).get_urls(in_preferred_only_ena, in_update_ena, in_credentials_ena)

    def get_annotated_cli_opts(self):
        """Return a basic/default connection details for this External service.
         example: {'host': '<host-ip>', 'username': 'admin', 'password': 'admin'}

        :return: host, port and default user to connect to this External service
        :rtype: dict
        """
        return {}

    def is_accessible(self, in_update_ena=False):
        """Whether External service can react to query of any kind.

        :return: True if External service is accessible
        :rtype: bool
        """
        return True

    def is_running(self, in_update_ena=False):
        """Whether External service is running (has PID).

        :return: True if External service has pid
        :rtype: bool
        """
        return True

    def status(self, in_update_ena=True):
        """Whether External service is accessible and running or not at all.

        :return: True if service is running and accessible, False otherwise
        :rtype: bool
        """
        return True

    def settle(self, in_stable_query_cnt=None, in_max_query_cnt=None, in_timeout=None, in_filter_method=None,
               in_verbose_ena=True):
        """Settling is not applicable to External Services."""
        return True

    def get_annotated_users(self, in_update_ena=True):
        raise NotImplementedError

