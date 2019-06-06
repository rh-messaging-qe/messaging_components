from iqa_common.ansible.ansible_inventory import AnsibleVirtualComponent
from messaging_abstract.component import Broker
from messaging_abstract.component.component import Component
from messaging_components.virtual.broker_cluster.abstract_broker_cluster import AbstractBrokerCluster

from .artemis_cluster import ArtemisCluster


class BrokerClusterFactory(object):

    @staticmethod
    def create_broker_cluster(implementation: str, vcomponent: AnsibleVirtualComponent, member_component: Component):

        for broker_cluster in AbstractBrokerCluster.__subclasses__():

            # Ignore broker with different implementation
            if broker_cluster.implementation != implementation:
                continue

            # If brokerCluster already exists, just append broker there, else create new BrokerClusterComponent
            if vcomponent.component is None:
                name = '%s-%s-%s' % ('broker_cluster', broker_cluster.__name__, vcomponent.name)
                broker_cluster_component = broker_cluster(name=name,
                                                          virtual_component=vcomponent,
                                                          member_component=member_component)
            else:
                # just add a member to existing component
                broker_cluster_component = vcomponent.component
                broker_cluster_component.add_member_component(member_component)  # type: AbstractBrokerCluster
                member_component.set_cluster_member(broker_cluster_component)  # type: Broker
            return broker_cluster_component

        raise ValueError('Invalid broker implementation: %s' % implementation)
