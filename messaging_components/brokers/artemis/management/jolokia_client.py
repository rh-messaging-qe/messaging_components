"""
Generic client for communicating with Jolokia API through POST requests.
"""

import requests
import json
import copy
import logging

from requests import ConnectionError, RequestException


class ArtemisJolokiaClientResult(Exception):
    """
    Wraps the response object providing a simpler representation.
    """
    def __init__(self):
        self.success = False
        self.error = None
        self.error_type = None
        self.data = None  # type: list
        self.response = None

    @staticmethod
    def from_jolokia_response(jolokia_response):
        res = ArtemisJolokiaClientResult()
        res.success = False
        res.error = None
        res.error_type = None
        res.data = None
        res.response = jolokia_response

        # If no jolokia_response provided
        if not jolokia_response:
            logging.getLogger().warning("Invalid Jolokia response => %s" % jolokia_response)
            res.error = 'Invalid Jolokia Response'
            return res

        # If not a valid JSON returned
        try:
            json_response = jolokia_response.json()
        except ValueError:
            logging.getLogger().exception("Invalid JSON returned")

        if 'error' in json_response:
            res.error = json_response['error']
            res.error_type = json_response['error_type']
            logging.getLogger().debug("Jolokia error_type = '%s' - error = '%s'"
                                      % (res.error_type, res.error))
            return res

        # At this point, response looks positive
        res.success = True
        return res

    @staticmethod
    def from_exception(exception):
        res = ArtemisJolokiaClientResult()
        res.success = False
        res.error = exception.__str__()
        res.error_type = None
        res.data = None
        res.response = None
        return res


class ArtemisJolokiaClient(object):
    """
    Provides a generic mechanism to query Jolokia API exposed by ActiveMQ Artemis.
    """
    def __init__(self, broker_name: str, ip: str, port: str, user: str, password: str):
        # Internal only
        self._ip = ip
        self._port = port
        self._user = user
        self._password = password

        # Request info (generic)
        self.type = 'exec'
        self.mbean = "org.apache.activemq.artemis:broker=\"%s\"" % broker_name

        # Must be defined by concrete requests
        self.operation = None
        self.arguments = None

    def list_queues(self, queue_name: str = '', exact: bool = False) -> ArtemisJolokiaClientResult:
        """
        Calls listQueues operation and returns queues matching filtering arguments
        through the data property of the returned object.
        :param queue_name:
        :param exact:
        :rtype: ArtemisJolokiaClientResult
        :return:
        """
        request = copy.copy(self)
        request.operation = "listQueues(java.lang.String,int,int)"
        filter_operation = 'CONTAINS' if not exact else 'EQUALS'
        request.arguments = ['{"field": "NAME", "operation": "%s", "value": "%s"}'
                             % (filter_operation, queue_name),
                             1,
                             100]

        return self._get_all_pages(request, 1)

    def list_addresses(self, address_name: str = '', exact: bool = False) -> ArtemisJolokiaClientResult:
        """
        Calls listAddresses operation and returns addresses matching filtering arguments
        through the data property of the returned object.
        :param address_name:
        :param exact:
        :return:
        """
        request = copy.copy(self)
        request.operation = "listAddresses(java.lang.String,int,int)"
        filter_operation = 'CONTAINS' if not exact else 'EQUALS'
        request.arguments = ['{"field": "NAME", "operation": "%s", "value": "%s"}' % (filter_operation, address_name),
                             1,
                             100]
        return self._get_all_pages(request, 1)

    def delete_address(self, name: str, force: bool = False) -> ArtemisJolokiaClientResult:
        """
        Deletes the given address.
        :param name: Address name
        :param force: Force address removal
        :return:
        """
        request = copy.copy(self)
        request.operation = "deleteAddress(java.lang.String,boolean)"
        request.arguments = [name, force]
        return self._execute(request)

    def delete_queue(self, name: str, remove_consumers: bool = False) -> ArtemisJolokiaClientResult:
        """
        Deletes the given queue.
        :param name: Queue name
        :param remove_consumers: Whether or not to remove connected consumers.
        :return:
        """
        request = copy.copy(self)
        request.operation = "destroyQueue(java.lang.String,boolean)"
        request.arguments = [name, remove_consumers]
        return self._execute(request)

    def create_address(self, name: str, routing_type: str='ANYCAST') -> ArtemisJolokiaClientResult:
        """
        Creates a new address
        :param name:
        :param routing_type:
        :return:
        """
        request = copy.copy(self)
        request.operation = "createAddress(java.lang.String,java.lang.String)"
        request.arguments = [name, routing_type]
        return self._execute(request)

    def create_queue(self, address_name: str, queue_name: str, durable: bool = True,
                     routing_type: str='ANYCAST') -> ArtemisJolokiaClientResult:
        """
        Creates a new queue nested to the provided Address
        :param address_name:
        :param queue_name:
        :param durable:
        :param routing_type:
        :return:
        """
        request = copy.copy(self)
        request.operation = "createQueue(java.lang.String,java.lang.String,boolean,java.lang.String)"
        request.arguments = [address_name, queue_name, durable, routing_type]
        return self._execute(request)

    def to_json(self):
        """
        Returns a JSON representation of the object.
        :return:
        """
        return json.loads(json.dumps(self, default=lambda x: x.__dict__))

    def _execute(self, request) -> ArtemisJolokiaClientResult:
        """
        Posts to the Jolokia API using the initialization arguments and
        returns a parsed ArtemisJolokiaClientResult object.
        :param request:
        :rtype: ArtemisJolokiaClientResult
        :return:
        """

        # Converts request to JSON representation
        json_request = request.to_json()

        # Debug info
        logging.getLogger().info("Posting to Jolokia API at: http://%s:%s/console/jolokia" % (self._ip, self._port))
        logging.getLogger().debug("Request => %s" % json_request)

        # Calling the Jolokia API
        try:
            response = requests.post('http://%s:%s/console/jolokia' % (self._ip, self._port),
                                     json=json_request,
                                     auth=(self._user, self._password))
            return ArtemisJolokiaClientResult.from_jolokia_response(response)
        except RequestException as ex:
            return ArtemisJolokiaClientResult.from_exception(ex)

    def _get_all_pages(self, request, page_arg_index):
        """
        Common private method to retrieve paged results from Jolokia API.
        :param request:
        :param page_arg_index:
        :return:
        """

        all_data = []
        result = None  # type: ArtemisJolokiaClientResult

        # Process all pages
        while True:
            result = self._execute(request)

            # If something wrong happened, stop processing
            if result.error:
                break

            json_res = result.response.json()

            # Expect 'value' key to be present
            if 'value' not in json_res:
                break

            # Returned value must have count and data
            value = json.loads(json_res['value'])
            total_queues = value['count']
            all_data.extend(value['data'])

            # In case all queues retrieve, skip
            if total_queues == 0 or total_queues == len(all_data):
                break

            # Increase page size and execute again
            request.arguments[page_arg_index] += 1

        if all_data and result:
            result.data = all_data

        return result
