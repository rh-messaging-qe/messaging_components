import json
import logging

import time
from requests import ConnectionError

from messaging_components.brokers.artemis import Utils
from messaging_components.brokers.artemis.ExternalBrokerOperable import ExternalBrokerOperable

LOGGER = logging.getLogger(__name__)


class ExternalBrokerOperableHA(ExternalBrokerOperable):
    """ Operable External High Availability broker class, which supports
    - gathering configuration data from input file
    - operations of this external broker (start, stop, status)
    - storing information about related master/slave brokers

    Note: Custom configuration change on the fly is not supported yet.
    """

    def __init__(self, in_fopts, in_testcontainer=None, in_opts=None):
        """Initialize HA broker SUT model to dschema object.

        :param in_fopts: framework options (should not be altered)
        :type in_fopts: dict
        :param in_testcontainer: current TestContainer (should not be altered)
        :type in_testcontainer: Test
        :param in_opts: options passed to self.opts (should not be altered)
        :type in_opts: dict
        """
        super(ExternalBrokerOperableHA, self).__init__(in_fopts, in_testcontainer, in_opts)
        self.is_master = False
        self.slave_broker = None
        self.master_broker = None

    def start(self, in_exp_result=True, as_service=True, wait_for_accessible=False, check_messaging=False):
        """Start operable broker object as service or as foreground process.
        Possibly wait for accessible broker state (via jolokia/Started call).

        :param in_exp_result: Expected result of start operation
        :type in_exp_result: bool
        :param as_service: whether to run as service or as foreground process
        :type as_service: bool
        :param wait_for_accessible: whether to wait for broker to start or not
        :type wait_for_accessible: bool
        :return: result of "running" operation or both running & accessible operations
        :rtype: bool
        """
        if as_service:
            cmd = "runuser -l %s %s start" % \
                  (self.opts.get('broker_ruser', 'jamq'),  # TODO(mtoth) platform dependent!
                   self._get_artemis_service_bin())
        else:
            # TODO(mtoth) needed?
            cmd = "runuser -l %s %s run" % \
                  (self.opts.get('broker_ruser', 'jamq'),  # TODO(mtoth) platform dependent!
                   self._get_artemis_bin())

        result = self.get_host().execute(cmd)
        result.wait_for_data()

        # normal daemon setup & run (as non-admin user -> runuser)
        self.test.add_run_and_report(result, in_exp_result)
        self._set_pid()

        if wait_for_accessible:
            if check_messaging:
                # forced check messaging OR broker is master
                retry_result = Utils.retry(self.is_accessible, True, max_count=60, max_duration=120)

            else:
                # not checking messaging OR broker is slave
                retry_result = Utils.retry(funct=lambda: self.is_accessible(check_messaging=False),
                                              expected_result=None, max_count=60, max_duration=120,
                                              check_funct=lambda a, b: a is not False)

            time.sleep(5)  # framework has to give slave broker some time to get proper topology updates
            self.test.add_check_and_report("Broker is accessible", retry_result[0])
            return retry_result[0]
        return self.is_running()


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

        if check_messaging and self.is_master:
            return status and Utils.service_ping(in_host=self.data.get_ssh_address(),
                                                 in_port=self.data.get_ports().get('artemis'))
        else:
            return status

    def get_ha_data(self):
        """Return HA related data for this broker from provided
        configuration file.

        :return: provided configuration data
        :rtype: HAData
        """
        return self.get_data().get_ha_data()

    def reset_topology(self):
        """Reset currently assigned master/slave broker
        and own master/slave role.
        """
        self.master_broker = None
        self.slave_broker = None
        self.is_master = False
