from collections import namedtuple
from typing import NamedTuple

from proton import Url
from proton.utils import BlockingConnection, SyncRequestResponse
import proton


class RouterQuery(object):
    """
    Provides methods that can be used to query the Dispatch Router.
    Connections are closed after each query.
    """
    def __init__(self, host="0.0.0.0", port=5672):
        self.host = host
        self.port = port

    def query(self, entity_type: str='org.apache.qpid.dispatch.router.node') -> NamedTuple:
        """
        Queries the related router instance, retrieving information for
        the provided Entity Type. The result is an array of a named tuple,
        whose fields are the attribute names returned by the router.
        In example, if querying entity type: org.apache.qpid.dispatch.allocator,
        the results can be accessed as: result.typeName, result.typeSize, ...
        same names returned by the router.
        :param entity_type:
        :return:
        """
        # URL to test
        url = Url("amqp://%s:%s/$management" % (self.host, self.port))

        # Proton connection
        connection = BlockingConnection(url, sasl_enabled=False)

        # Proton sync client
        client = SyncRequestResponse(connection, url.path)

        # Request message object
        request = proton.Message()
        request.properties = {u'operation': u'QUERY', u'entityType':u'%s' % entity_type}
        request.body = {u'attributeNames':[]}

        # Sending the request
        response = client.call(request)

        # Closing connection
        client.connection.close()

        # Namedtuple that represents the query response from the router
        # so fields can be read based on their attribute names.
        RouterQueryResults = namedtuple('RouterQueryResults', response.body["attributeNames"])
        records = []

        for record in response.body["results"]:
            records.append(RouterQueryResults(*record))

        return records

    def listener(self):
        return self.query(entity_type='org.apache.qpid.dispatch.listener')

    def connector(self):
        return self.query(entity_type='org.apache.qpid.dispatch.connector')

    def router(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router')

    def address(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.address')

    def config_address(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.address')

    def config_autolink(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.autoLink')

    def config_linkroute(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.linkRoute')

    def config_exchange(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.exchange')

    def config_binding(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.config.binding')

    def node(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.node')

    def ssl_profile(self):
        return self.query(entity_type='org.apache.qpid.dispatch.sslProfile')

    def connection(self):
        return self.query(entity_type='org.apache.qpid.dispatch.connection')

    def allocator(self):
        return self.query(entity_type='org.apache.qpid.dispatch.allocator')

    def log_stats(self):
        return self.query(entity_type='org.apache.qpid.dispatch.logStats')

    def router_link(self):
        return self.query(entity_type='org.apache.qpid.dispatch.router.link')

    def policy(self):
        return self.query(entity_type='org.apache.qpid.dispatch.policy')

    def vhost(self):
        return self.query(entity_type='org.apache.qpid.dispatch.vhost')

    def vhost_user_group_settings(self):
        return self.query(entity_type='org.apache.qpid.dispatch.vhostUserGroupSettings')

    def vhost_stats(self):
        return self.query(entity_type='org.apache.qpid.dispatch.vhostStats')

    def auth_service_plugin(self):
        return self.query(entity_type='org.apache.qpid.dispatch.authServicePlugin')

    def configuration_entity(self):
        return self.query(entity_type='org.apache.qpid.dispatch.configurationEntity')

    def log(self):
        return self.query(entity_type='org.apache.qpid.dispatch.log')

    def console(self):
        return self.query(entity_type='org.apache.qpid.dispatch.console')

    def management(self):
        return self.query(entity_type='org.apache.qpid.dispatch.management')
