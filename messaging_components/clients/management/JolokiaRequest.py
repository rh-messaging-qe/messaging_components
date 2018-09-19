"""JolokiaRequest class to perform various simple jolokia
request-reponse operations."""

import logging
import copy
import json
from string import Template
import requests

from messaging_components.brokers.artemis import ExternalBroker

LOGGER = logging.getLogger(__name__)


class JolokiaRequest(object):
    """This class makes a small abstraction over usage of jolokia calls
    via 'requests' modules for AMQ 7 broker. By default this client supports
    AMQ7 with old style of dtests deployment (sut models etc..)
    and new style using ExternalBroker.

    Just provide necessary operations information to create correct jolokia call
    and get resulting data. Default messaging information (url, port, users)
    will be taken from provided broker service. To get the full jolokia url,
    pick an operation you need to call via Artemis web UI, mimic it's REST url
    and divide it according provided template.

    For details see official Artemis documentation
    https://activemq.apache.org/artemis/docs/latest/management.html

    .. note:
    7.1.0 AMQ7 used 'hawtio' as root context, later it changed to 'console'

    .. example:
    (artificially divided URL on multiple lines)::
    http://127.0.0.1:8161/console/jolokia/read/
    org.apache.activemq.artemis:broker=amq
    ,component=addresses,address=%22activemq.notifications%22
    ,subcomponent=queues,routing-type=%22multicast%22\
    ,queue="notif.2f8b91d0.ActiveMQServerImpl_serverUUID=27a41af0"/ObjectName

    ---> ::

    JolokiaRequest(
        self.i_cs['server.messaging-service'],
        query_operation='read',
        component=',component=addresses,address="activemq.notifications"'
        subcomponent=',subcomponent=queues,routing-type="......UUID=27a41af0'
        operation='/ObjectName'
    )
    """
    DEFAULT_JOLOKIA_PORT = 8161
    DEFAULT_BROKER_NAME = 'amq'
    CONSOLE_NAME = 'console'
    OLD_CONSOLE_NAME = 'hawtio'

    def __init__(self, broker_service, query_operation, operation,
                 component='', subcomponent='', username='admin'):
        """Prepare base template of Jolokia call from given SUT model.

        :param broker_service: AMQ7/Artemis sut model or ExternalBroker (AMQ7/Artemis)
        :type broker_service: dtestlib.sut_models.Artemis1Broker | dtestlib.sut.ExternalBroker.ExternalBroker
        :param query_operation: base operation exec/read/.. etc (set?)
        :type query_operation: str
        :param operation: final operation method at the end of original jolokia call (Browse())
        :type operation: str
        :param component: component path defined via string
        :type component: str
        :param subcomponent: subcomponent path defined via string
        :type subcomponent: str
        :param username: jolokia/web user (default admin)
        :type username: str
        :param password: password for jolokia/web user (default admin)
        :type password: str
        """
        self.response = None

        if isinstance(broker_service, ExternalBroker):
            self.host = broker_service.get_data().get_ssh_address()
            self.port = broker_service.get_data().get_ports().get('web')
            self.broker_name = broker_service.get_data().get_instance_name()
            self.username = broker_service.get_data().get_admin_user()
            self.password = broker_service.get_data().get_admin_password()

        self.template = {'HOST': self.host,
                         'PORT': self.port,
                         'QUERY_OPERATION': query_operation,
                         'BROKER_NAME': self.broker_name,
                         'COMPONENT': component,
                         'SUBCOMPONENT': subcomponent,
                         'OPERATION': operation}

    def do_request(self, console_name="console"):
        """Do request/response call on broker via provided jolokia call

        :param console_name: optional parameter to query context root 'console' or 'hawtio'
        :type console_name: str
        """
        template_read_operation = Template(
            'http://${HOST}:${PORT}/${CONTEXT_ROOT}/jolokia/${QUERY_OPERATION}'
            '/org.apache.activemq.artemis:broker="${BROKER_NAME}"${COMPONENT}${SUBCOMPONENT}${OPERATION}'
        )

        active_template = copy.deepcopy(self.template)
        active_template['CONTEXT_ROOT'] = console_name

        request_operation = template_read_operation.substitute(active_template)
        LOGGER.info("Request='%s', '%s':'%s'", request_operation, self.username, self.password)

        response = requests.get(request_operation, auth=(self.username, self.password), timeout=10)

        if response.status_code == requests.codes.not_found:  # 404
            # retry the same operation with different hawtio as base_uri instead of console
            LOGGER.warn("Trying context root '%s' instead of '%s'.", self.OLD_CONSOLE_NAME, self.CONSOLE_NAME)
            self.response = self.do_request(self.OLD_CONSOLE_NAME)
            return response

        self.response = response
        return response

    @property
    def response_data_as_json(self):
        """Return final response text as json object

        :rtype: dict
        """
        return json.loads(self.response.text)

    def get_response_content_as_json(self):
        """Return request content as json object

        :rtype: dict
        """
        return self.response.json()

    def get_response_content_value_as_json(self):
        """Return final value of request content as json object

        :rtype: dict
        """
        return self.response.json().get('value')

    @property
    def status(self):
        """Status error code of this call

        :rtype: int
        """
        return self.response.status_code
