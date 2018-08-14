"""
    # TODO jstejska: Fill package info
"""

import copy
import reformat
from optconstruct.types import BasicComposed


class BrokerURLnodeJS(BasicComposed):
    """BrokerURL option construct class for nodeJS messaging client."""

    composed_keys = {'host'}

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

        credentials = reformat.reformat("%{user|%s}%{password|:%s}", data)

        if credentials:
            data_copy = copy.deepcopy(data)
            data_copy['credentials'] = credentials
        else:
            data_copy = data

        pattern = self._postprocessing("%{credentials|%s@}%{host}%{port|:%s}")
        broker_url = self.prefix + " " + reformat.reformat(pattern, data_copy)

        return broker_url

