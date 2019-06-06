import abc
import os
import posixpath

import dpath
import logging
import yaml

from messaging_abstract.component import Component, Broker
from messaging_components.node import NodeAnsible, CommandAnsible, NodeLocal, NodeDocker, Command

LOGGER = logging.getLogger(__name__)


class IQAConfigurationException(Exception):

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super(IQAConfigurationException, self).__init__(message)


class Utils(object):

    @staticmethod
    def remove_prefix(str, prefix):
        if str.startswith(prefix):
            return str[len(prefix):]
        else:
            return str


class Config(object):
    """Placeholder class of read configuration details from provided input file.
    Input file is json supported only (yaml in the future).
    """
    LOGGER = logging.getLogger(__name__)
    config_file = 'data_config_file'
    original_config_file = None
    local_config_dir = None  # local cconfiguration directory (ansible inventory dir)
    node_config_dir = None  # remote configuration directory
    object_list = []
    yaml_data = None
    old_yaml_data = None  # re|store configuration data

    def __init__(self, component: Component, **kwargs):
        self.component = component

        if self.config_file in kwargs.keys():
            print(kwargs.get(self.config_file))
            self.original_config_file = kwargs.get(self.config_file)
            self.create_configuration(self.original_config_file)
        else:
            self.create_default_configuration(**kwargs)
            LOGGER.info("No configuration file provided, using defaults")

        # ansible synchronize must have trailing "/" to sync dir-content
        # TODO inventory is not part of Executor (this is not generic)
        # self.local_config_dir = posixpath.join(os.path.dirname(component.executor.inventory), component.name, "")

    def _data_getter(self, path, default=None):
        """General function to query data from provided external data dictionary.

        :param path: internal path to query data (broker_xml/journal/persistence_enabled)
        :type path: str
        :param default: what to return if value not find based on key-path
        :type default: int | str | list | dict | None
        :return: found value from provided key path
        :rtype: int | str | list | dict
        """
        try:
            output = dpath.get(self.yaml_data, path)
            # LOGGER.debug("Dpath_search=%s\n%s" % (path, output))
        except (KeyError, ValueError) as exc:
            LOGGER.debug('Unknown key or value %s', path)
            return default
        return output

    def load_configuration_yaml(self, path):
        """Load provided configuration YAML file.

        :param path: path to configuration file
        :type path: str
        :return: List of initialized messaging servers (as objects)
        :rtype: list
        """
        with open(path, 'r') as f:
            try:
                self.yaml_data = yaml.full_load(f)
            except yaml.YAMLError as exc:
                raise IQAConfigurationException("Unable to load file '%s' for '%s'" % (path, self.__class__.__name__))

            if "artemis" not in self.yaml_data['render']['template']:
                raise IQAConfigurationException("Incompatible data structure for %s !" % (self.__class__.__name__))

    @abc.abstractmethod
    def load_configuration(self):
        pass

    @abc.abstractmethod
    def create_configuration(self, config_file_path):
        pass

    @abc.abstractmethod
    def apply_config(self, yaml_configuration):
        pass

    @abc.abstractmethod
    def create_default_configuration(self, **kwargs):
        pass

    def restore_config(self):
        self.apply_config(self.original_config_file)

    def copy_configuration_files(self):
        cmd_copy_files = None
        if isinstance(self.component.node, NodeAnsible):
            cmd_copy_files = CommandAnsible(ansible_module="synchronize",
                                            ansible_args='src=%s dest=%s' % (self.local_config_dir,
                                                                             self.node_config_dir),
                                            stdout=True,
                                            stderr=True,
                                            timeout=20)
        elif isinstance(self.component.node, NodeLocal):
            cmd_copy_files = Command([], stdout=True, timeout=20)
        elif isinstance(self.component.node, NodeDocker):
            raise IQAConfigurationException("Unable to change configuration on docker node")

        return self.component.node.execute(cmd_copy_files)
