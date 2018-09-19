from messaging_components.brokers import Broker

class AbstractExternal(Broker):
    """Abstract External broker (JAMQ7/Artemis) API for various services.

    For now, this class inherits from JAMQ7Broker DSchema, but in future,
    it can be object on its own, separate to DSchema.
    """

    def __init__(self, in_fopts, in_testcontainer=None, in_opts=None):
        """Initialize SUT model to dschema objects.

        :param in_fopts: framework options (should not be altered)
        :type in_fopts: dict
        :param in_testcontainer: current TestContainer (should not be altered)
        :type in_testcontainer: Test
        :param in_opts: options passed to self.opts (should not be altered)
        :type in_opts: dict
        """
        # super(AbstractExternal, self).__init__(in_fopts, in_testcontainer=None, in_opts=None)
        self.msg_processor = None

    def start(self, in_exp_result=True):
        """Start external service.

        Might not be implemented for "external services".

        :param in_exp_result: expected result of this function
        :type in_exp_result: bool
        :return: success of starting given service
        :rtype: bool
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def restart(self, as_service=True):
        """Restart external service.

        Might not be implemented for "external services".
        :param as_service: whether do restart via service or otherwise
        :type as_service: bool
        :return: success of restarting given service
        :rtype: bool
        """
        raise NotImplementedError

    def cfg_apply(self):
        """Apply new configuration to External service.

        Not applicable for majority of External services

        :return: success of applying new configuration to External service
        :rtype: bool
        """
        raise NotImplementedError

    def cfg_apply_dynamic(self):
        """Apply new configuration to External service without any restart to service (reload config).

        Not applicable for majority of External services

        :return: success of applying new configuration to External service
        :rtype: bool
        """
        raise NotImplementedError

    def cfg_revert(self, in_exp_result=True):
        """Apply original/previous configuration to External service.

        Not applicable for majority of External services

        :return: success of applying original/previous configuration to External service
        :rtype: bool
        """
        raise NotImplementedError

    def cfg_status(self):
        """Status of applying configuration.

        Not applicable for majority of External services

        :return: configuration status of External service
        :rtype: bool
        """
        raise NotImplementedError

    def is_accessible(self, in_update_ena=False):
        """Whether External service can react to query of any kind.

        :return: True if External service is accessible
        :rtype: bool
        """
        raise NotImplementedError

    def is_running(self, in_update_ena=False):
        """Whether External service is running (has PID).

        :return: True if External service has pid
        :rtype: bool
        """
        raise NotImplementedError

    def status(self, in_update_ena=True):
        """Whether External service is accessible and running or not at all.

        :return: True if service is running and accessible, False otherwise
        :rtype: bool
        """
        raise NotImplementedError

    def settle(self, in_stable_query_cnt=None, in_max_query_cnt=None, in_timeout=None, in_filter_method=None,
               in_verbose_ena=True):
        """Settling is not applicable to External Services."""
        # TODO to be removed (?)
        raise NotImplementedError

    def get_state(self, in_update_ena=False):

        """Return state of the broker - assume all is OK for now - External service.

        :param in_update_ena: Method not used, just because of backwards compatibility.
        :type in_update_ena: bool
        :return: Assume everything is ok with broker objects
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
        raise NotImplementedError

    def get_port(self, in_type='amqp'):
        """Return port number of given service type of External service.

        Might not be implemented for "external services".

        :param in_type: Type of service running on External service
        :type in_type: str
        :return: port number of service running on External service
        :rtype: int
        """
        raise NotImplementedError

    def get_ports(self, in_preferred_only_ena=False, in_update_ena=False):
        """Get ports for this broker (SUT model)

        :param in_preferred_only_ena: returns 'main' port
        :type in_preferred_only_ena: bool
        :param in_update_ena: force broker state update - INVALID
        :type in_update_ena: bool
        :return: list of selected ports
        :rtype: list[int]
        """
        raise NotImplementedError

    def get_annotated_ports(self, in_update_ena=False):
        """Return a mapping of port and running services on External service.

        :param in_update_ena: not used (only for inheritance backwards compatibility here)
        :type in_update_ena: bool
        :return: mapping for service type : port for External service
        :rtype: dict
        """
        raise NotImplementedError

    def get_annotated_dirs(self, in_update_ena=False):
        """Return information about configuration directories of External service.

        :return: return External service directories
        :rtype: dict
        """
        raise NotImplementedError

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
        raise NotImplementedError

    def get_annotated_cli_opts(self):
        """Return a basic/default connection details for this External service.

        :return: host, port and default user to connect to this External service
        :rtype: dict
        """
        raise NotImplementedError

    def get_annotated_users(self, in_update_ena=True):
        """Return users with passwords and other needed
        credential details for Authentication to External service.

        :return: users mapping with their credentials information
        :rtype: dict
        """
        raise NotImplementedError

    def get_cli_opts(self):
        """Return default client options for given External service

        :return: current client options
        :rtype: dict
        """
        raise NotImplementedError
