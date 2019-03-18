import logging
from typing import List

from iqa_common.executor import Executor
from messaging_abstract.component import Queue, Address
from messaging_abstract.component.server.broker import Broker
from messaging_abstract.component.server.broker.route import RoutingType
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node

import messaging_components.protocols as protocols
from messaging_components.brokers.artemis.management import ArtemisJolokiaClient


class Artemis(Broker):
    """
    Apache ActiveMQ Artemis has a proven non blocking architecture. It delivers outstanding performance.
    """

    supported_protocols = [protocols.Amqp10(), protocols.Mqtt(), protocols.Stomp(), protocols.Openwire()]
    name = 'Artemis'
    implementation = 'artemis'

    def __init__(self, name: str, node: Node, executor: Executor, service: Service, **kwargs):
        super(Artemis, self).__init__(name, node, executor, service, **kwargs)
        self._queues: List[Queue] = list()
        self._addresses: List[Address] = list()
        self._addresses_dict = {}

    def queues(self, refresh: bool=True) -> List[Queue]:
        """
        Retrieves and lists all queues
        :param refresh:
        :return:
        """
        if self._queues and not refresh:
            return self._queues

        self._refresh_addresses_and_queues()
        return self._queues

    def addresses(self, refresh: bool=True) -> List[Address]:
        """
        Retrieves and lists all addresses
        :param refresh:
        :return:
        """
        if self._addresses and not refresh:
            return self._addresses

        self._refresh_addresses_and_queues()
        return self._addresses

    def create_address(self, address: Address):
        """
        Creates the given address
        :param address:
        :return:
        """
        client = self._get_management_client()
        routing_type = self._get_routing_type(address.routing_type)
        return client.create_address(address.name, routing_type)

    def create_queue(self, queue: Queue, address: Address, durable: bool = True):
        """
        Creates a given queue based on provided arguments
        :param queue:
        :param address:
        :param durable:
        :return:
        """
        client = self._get_management_client()
        if queue.routing_type == RoutingType.BOTH:
            raise ValueError('Queues can only use ANYCAST or MULTICAST routing type')
        return client.create_queue(address.name, queue.name, durable, queue.routing_type.name)

    def delete_address(self, name: str, force: bool = False):
        """
        Deletes an address
        :param name:
        :param force:
        :return:
        """
        client = self._get_management_client()
        return client.delete_address(name, force)

    def delete_queue(self, name: str, remove_consumers: bool = False):
        """
        Deletes a queue
        :param name:
        :param remove_consumers:
        :return:
        """
        client = self._get_management_client()
        return client.delete_queue(name, remove_consumers)

    def _refresh_addresses_and_queues(self):
        """
        Need to combine both calls, in order to map queues to addresses
        and vice-versa.
        :return:
        """
        # Retrieving queues
        queues = list()
        addresses = list()

        # Get a new client instance
        client = self._get_management_client()
        queues_result = client.list_queues()
        addresses_result = client.list_addresses()

        # In case of errors, return empty list
        if not queues_result.success:
            logging.getLogger().warning('Unable to retrieve queues')
            return

        # In case of errors, return empty list
        if not addresses_result.success:
            logging.getLogger().warning('Unable to retrieve addresses')
            return

        # Dictionary containing retrieved addresses
        addresses_dict = {}

        # If no address found, skip it
        if not addresses_result.data:
            logging.debug("No addresses available")
        else:
            # Parsing returned addresses
            for addr_info in addresses_result.data:
                logging.debug("Address found: %s - routingType: %s" % (addr_info['name'], addr_info['routingTypes']))
                address = Address(name=addr_info['name'],
                                  routing_type=RoutingType.from_value(addr_info['routingTypes']))
                addresses_dict[address.name] = address
                addresses.append(address)

        # If no queues returned
        if not queues_result.data:
            logging.debug("No queues available")
        else:
            # Parsing returned queues
            for queue_info in queues_result.data:
                logging.debug("Queue found: %s - routingType: %s" % (queue_info['name'], queue_info['routingType']))
                routing_type = RoutingType.from_value(queue_info['routingType'])
                address = addresses_dict[queue_info['address']]
                queue = Queue(name=queue_info['name'],
                              routing_type=routing_type,
                              address=address)
                queue.message_count = queue_info['messageCount']
                address.queues.append(queue)
                queues.append(queue)

        # Updating broker data
        self._addresses_dict = addresses_dict
        self._addresses = addresses
        self._queues = queues

    def _get_management_client(self):
        """
        Creates a new instance of the Jolokia Client.
        :return:
        """
        client = ArtemisJolokiaClient(self.broker_name, self.node.get_ip(), self.web_port,
                                      self.user, self.password)
        return client

    def _get_routing_type(self, routing_type: RoutingType) -> str:
        """
        Returns the routing type str value, based on expected values on the broker.
        :param routing_type:
        :return:
        """
        if routing_type == RoutingType.BOTH:
            return 'ANYCAST, MULTICAST'
        return routing_type.name

