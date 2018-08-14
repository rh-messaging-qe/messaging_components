"""
    # TODO jstejska: Fill package info
"""

import copy
import reformat
from optconstruct.types import BasicComposed


class BrokerURLPythonProton(BasicComposed):
    """BrokerURL option parser for Proton-Python messaging client."""

    composed_keys = {'host', 'port', 'address'}

    def satisfied(self, data: dict):
        """Check if client's option should be generated.

        :param data: data with specified option's values
        :type data: dict
        :return: True or False
        :rtype bool
        """

        return bool(set(data.keys()).intersection(self.composed_keys))

    def generate(self, data, client=None):
        """Generate option brokerURL option.

        :param data: data with specified option's values
        :type data: dict
        :param client: client's label
        :type client: str
        :return: option
        :rtype: str
        """
        _ = client

        broker_url = data.get('broker-url', None)

        if broker_url is not None:
            broker_url = self.prefix + " " + broker_url
            return broker_url

        pattern = "%{user|%s}%{password|:%s}"

        credentials = reformat.reformat(pattern, data)

        if credentials:
            data_copy = copy.deepcopy(data)
            data_copy['credentials'] = credentials
        else:
            data_copy = data

        pattern = self._postprocessing("%{credentials|%s@}%{host}%{port|:%s}%{address|/%s}")
        broker_url = self.prefix + " " + reformat.reformat(pattern, data_copy)

        return broker_url
