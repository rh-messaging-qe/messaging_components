import json
import logging
import requests
from requests import ConnectionError

from messaging_components.brokers.artemis import Utils
from messaging_components.brokers.artemis.AbstractExternal import AbstractExternal

LOGGER = logging.getLogger(__name__)


class ExternalBroker(AbstractExternal):
    """External broker, which is capable of having configuration read from file
    and basic accessibility check.

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
        super(ExternalBroker, self).__init__(in_fopts, in_testcontainer, in_opts)
        self.data = None
        self.pid = None
        self.associated_nodes = None

    # ================ dumb override of methods for no checking of status
    def start(self, in_exp_result=True, as_service=True):
        return NotImplementedError

    def stop(self, in_killsig_id=0, in_stop_all_brokers_on_node=False, as_service=True):
        return NotImplementedError

    def restart(self, as_service=True):
        pass

    def cfg_apply(self):
        pass

    def cfg_apply_dynamic(self):
        pass

    def cfg_revert(self, in_exp_result=True):
        pass

    def cfg_status(self):
        return True

    def is_accessible(self, in_update_ena=False, check_messaging=True):
        """Contact broker via jolokia and request result of "Started" operation.

        :param in_update_ena: Not used/invalid (backwards compatibility
        :type in_update_ena: bool
        :param check_messaging: Whether to check for messaging subsystem up or not (HA slave scenarios)
        :type check_messaging: bool
        :return: whether broker is accessible or not through jolokia call
        :rtype: bool
        """
        # http://<host>:8161/console/jolokia/read/org.apache.activemq.artemis:broker=%22amq%22/Started
        status_template_dict = {'HOST': self.data.get_ssh_address(),
                                'PORT': self.data.get_ports().get('web'),
                                'QUERY_OPERATION': 'read',
                                'BROKER_NAME': self.data.get_instance_name(),
                                'OPERATION': '/Started'
                                }
        try:
            response_data = self.do_read_request(status_template_dict)
            LOGGER.debug("response_text=%s" % response_data.text)
            status = json.loads(response_data.text).get('value')
        except ConnectionError as ce:
            LOGGER.debug("Unable to connect to broker on %s. %s" % (self.data.get_ssh_address(), ce))
            status = False

        if check_messaging:
            pinged = Utils.service_ping(in_host=self.data.get_ssh_address(),
                                        in_port=self.data.get_ports().get('artemis'))
            return status and pinged
        else:
            return status

    def is_running(self, in_update_ena=False):
        return True

    def status(self, in_update_ena=True):
        return True

    def settle(self, in_stable_query_cnt=None, in_max_query_cnt=None, in_timeout=None, in_filter_method=None,
               in_verbose_ena=True):
        return True

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def set_settings_data(self, settings_data):
        """Set provided data to this broker object

        :param settings_data: configuration data provided from file
        :type settings_data: dtestlib.sut.ExternalBrokerData
        """
        self.data = settings_data
        self.get_associated_nodes()

    def get_data(self):
        """Return data associated to this broker object.

        :return: configuration data provided from file
        :rtype: dtestlib.sut.ExternalBrokerData
        """
        return self.data

    def get_ssh_address(self):
        """Return default address for connection

        :return: IP of hostname provided in configuration
        :rtype: str
        """
        return self.data.get_ssh_address()

    def get_host(self):
        """Return associated TestNode for given broker.

        :return: TestNode broker is running on
        :rtype: dtestlib.TestNode
        """
        return self.data.get_test_node()

    def get_pid(self, in_update_ena=False):
        """Get pid number for currently running broker.
        Should be always actual.

        :param in_update_ena: not used (only for inheritance backwards compatibility here)
        :type in_update_ena: bool
        :return:
        :rtype: int
        """
        return self.pid

    def get_port(self, in_type='artemis'):
        return self.get_annotated_ports().get(in_type)

    def get_ports(self, in_preferred_only_ena=False, in_update_ena=False):
        """Get ports for this broker (SUT model)

        :param in_preferred_only_ena: returns 'artemis' port
        :type in_preferred_only_ena: bool
        :param in_update_ena: force broker state update - INVALID
        :type in_update_ena: bool
        :return: list of selected ports
        :rtype: list[int]
        """
        if in_preferred_only_ena:
            return [self.data.get_ports().get('artemis')]
        else:
            return list(set(self.data.get_ports()))

    def get_annotated_ports(self, in_update_ena=False):
        """Return a mapping of port and running services on External service.

        :param in_update_ena: not used (only for inheritance backwards compatibility here)
        :type in_update_ena: bool
        :return: mapping for service type : port for External service
        :rtype: dict
        """
        return self.data.get_ports()

    def get_annotated_dirs(self, in_update_ena=False):
        """Return information about configuration directories of External service.

        :return: return External service directories
        :rtype: dict
        """
        return {'paths': {'base-dir': self.data.get_home(),
                          'inst-dir': self.data.get_instance_home(),
                          'cfg-dir': self.data.get_instance_conf_dir()
                          }
                }

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
        # TODO broker url from TestNode that is assigned. Remove this method?
        return self.data.get_ssh_address()

    def get_url(self, port_name='artemis'):
        """Return service url for this broker for given service amqp/openwire/artemis acceptors.

        :param port_name: name of the port to be retrieved
        :type port_name: str
        :return: service url with specified port_name of default one
        :rtype: str
        """
        return "%s:%s" % (self.data.get_ssh_address(), self.get_port(port_name))

    def get_cli_opts(self):
        """Return default client options for given External service

        :return: current client options
        :rtype: dict
        """
        return {}

    def get_annotated_cli_opts(self):
        """Provide information for client to connect to this broker.

        :return: dict of needed client options (host, port, broker name, default users)
        :rtype: dict
        """
        # TODO get 'host' from TestNode object that is assigned to this broker model
        external_cli_opts = {'host': self.data.get_ssh_address(),
                             'port': self.data.get_ports(),
                             'broker-name': self.data.get_instance_name()}
        external_cli_opts.update(**self.data.get_users_plain_dtests_format())
        return external_cli_opts

    def get_annotated_users(self, in_update_ena=True):
        users = self.data.get_users()
        annotated_users = {}
        for user in self.users:
            annotated_users[user.username] = {}
            annotated_users[user.username]['password'] = user.password
            annotated_users[user.username]['roles'] = user.roles
        return annotated_users

    def get_associated_nodes(self):
        """This returns a dictionary pair of internal brokerNodeID and IP.
        For cluster host6 is following output

        {'9e5bee31-31fa-11e8-b59f-5254003da80d': '<host1>\\/<host1>:61616',
         '9e6563f4-31fa-11e8-9da3-5254004e96d5': '<host2>\\/<host2>:61616',
         '9e81780b-31fa-11e8-8a79-525400b22d8e': '<host3>\\/<host3>:61616',
         '9e82fec4-31fa-11e8-82ab-52540045bbb8': '<host4>\\/<host4>:61616',
         '9fb73893-31fa-11e8-bb2d-525400f1f81a': '<host5>\\/<host5>:61616'}

        :return: mapping of internal brokerIDs and hosts in cluster
        :rtype: dict
        """
        return self.associated_nodes

    def set_associated_nodes(self, nodes):
        """Set paired associated nodes of this broker in cluster.
        See get_associated_nodes() for details about format.

        :param nodes: test node running associated broker
        :type nodes: dict
        """
        self.associated_nodes = nodes

    def do_read_request(self, request_template_dict, console_name="console"):
        """Do request/response call on broker

        :param request_template_dict: Template fill with data (see example)
        {'host': self.data.get_ssh_address(),
         'port': 8161,
          'query_operation': 'read'
          'broker_name': self.data.get_instance_name(),
          'operation': 'Started'
          }
        :type request_template_dict:
        :param console_name: whether to use 'console' or 'hawtio' for jolokia query as base uri
        :type console_name: str
        :return: whole raw response
        :rtype: request.api.response
        """
        from string import Template

        template_read_operation = Template(
            'http://${HOST}:${PORT}/%s/jolokia/${QUERY_OPERATION}'
            '/org.apache.activemq.artemis:broker="${BROKER_NAME}"${OPERATION}' % console_name)

        username = self.get_data().get_admin_user().username
        password = self.get_data().get_admin_password()

        request_operation = template_read_operation.substitute(request_template_dict)
        LOGGER.debug("Request=%s, %s:%s" % (request_operation, username, password))
        response = requests.get(request_operation, auth=(username, password), timeout=10)

        if response.status_code == 404:
            # retry the same operation with different hawtio as base_uri instead of console
            LOGGER.warn("Trying context root 'hawtio' instead 'console'")
            response = self.do_read_request(request_template_dict, "hawtio")
        elif response.status_code != 200:
            LOGGER.warn('Unexpected failure in jolokia call reason: "%s %s"',
                        response.status_code, response.reason)
        return response
