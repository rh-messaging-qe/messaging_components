from iqa_common.ansible.ansible_inventory import AnsibleVirtualComponent
from messaging_abstract.component.component import Component

from messaging_abstract.component.server.broker import Broker
from messaging_abstract.component.server.service import Service
from messaging_abstract.node.node import Node
from typing import List
import abc
import logging


class AbstractBrokerCluster(Component, abc.ABC):
    """
    Abstract broker cluster class
    """
    supported_protocols = []
    cluster_members = []
    cluster_group_name = None
    required_fields = ['broker_cluster_group']
    service = None

    def __init__(self, name: str, virtual_component: AnsibleVirtualComponent, member_component: Component):
        for field in self.required_fields:
            if field not in virtual_component.kwargs:
                logging.error("Missing required broker cluster parameter: %s" % field)
                raise AttributeError("Missing required field 'broker_cluster_group'!")

        super(AbstractBrokerCluster, self).__init__(name, member_component.node, member_component.executor)

        self.add_member_component(member_component)  # Add initial member (broker) to cluster
        member_component.set_cluster_member(self) # Broker
        self.service = member_component.service  # Todo change to "custom_service" and cluster status?
        self.cluster_group_name = virtual_component.kwargs.get('broker_cluster_group')

    def add_member_component(self, component):
        self.cluster_members.append(component)

    @abc.abstractmethod
    def get_cluster_group_name(self) -> str:
        raise NotImplementedError()

    def get_brokers(self) -> List[Broker]:
        return self.cluster_members

    @abc.abstractmethod
    def get_running_brokers(self) -> List[Broker]:
        raise NotImplementedError()

    @abc.abstractmethod
    def reset_topology(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_topology(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_default_broker(self) -> Broker:
        raise NotImplementedError()

    # Optional methods
    # @abc.abstractmethod
    # def kill(self, signal, broker) -> bool:
    #     raise NotImplementedError()

    @abc.abstractmethod
    def get_associated_nodes(self) -> List[Node]:
        raise NotImplementedError()
