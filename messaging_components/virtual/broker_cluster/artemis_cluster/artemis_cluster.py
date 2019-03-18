import logging
from typing import List

from iqa_common.ansible.ansible_inventory import AnsibleVirtualComponent
from iqa_common.executor import Executor
from messaging_abstract.component import Broker, Queue, Address
from messaging_components.virtual.broker_cluster.abstract_broker_cluster import AbstractBrokerCluster
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node

import messaging_components.protocols as protocols
from messaging_components.brokers.artemis.management import ArtemisJolokiaClient


class ArtemisCluster(AbstractBrokerCluster):
    """
    Apache ActiveMQ Artemis has a proven non blocking architecture. It delivers outstanding performance.
    """
    supported_protocols = [protocols.Amqp10(), protocols.Mqtt(), protocols.Stomp(), protocols.Openwire()]
    name = 'artemis_cluster'
    implementation = 'artemis_cluster'
    members = list()

    def __init__(self, name: str, virtual_component: AnsibleVirtualComponent, member_component):
        super(ArtemisCluster, self).__init__(name, virtual_component, member_component)
        self.default_broker = member_component
        self.virtual_component = virtual_component
        self.virtual_component.component = self

    def get_cluster_group_name(self) -> str:
        pass

    def get_running_brokers(self) -> List[Broker]:
        pass

    def reset_topology(self) -> bool:
        pass

    def update_topology(self) -> bool:
        pass

    def get_default_broker(self) -> Broker:
        return self.default_broker

    def get_associated_nodes(self) -> List[Node]:
        pass
