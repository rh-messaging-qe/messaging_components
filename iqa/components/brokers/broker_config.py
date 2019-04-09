import abc

from iqa.abstract.components.component import Component
from iqa.abstract.components.configuration import Configuration


class BrokerConfiguration(Configuration):

    users = {}
    ports = {}

    def __init__(self, component: Component, **kwargs):
        super(BrokerConfiguration, self).__init__(component, **kwargs)

    @abc.abstractmethod
    def assign_ports(self):
        pass

    @abc.abstractmethod
    def create_default_configuration(self, **kwargs):
        pass

    @abc.abstractmethod
    def get_users(self):
        pass

    @abc.abstractmethod
    def get_acceptors(self):
        pass

    get_listeners = get_acceptors

    @abc.abstractmethod
    def apply_config(self, yaml_configuration):
        pass
