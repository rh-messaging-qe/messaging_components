#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import _Section, _Attribute


class addrPort(_Section):
    """
    Attributes for internet address and port.
    Used by: listener, connector.
    """
    section_name = 'addrPort'
    used_by = ['listener', 'connector']

    def __init__(self, host=None, port=None, protocolFamily=None, name=None):
        """
        :param host: IP address: ipv4 or ipv6 literal or a host name
        :type host: string

        :param port: Port number or symbolic service name.
        :3type port: string

        :param protocolFamily: IPv4: Internet Protocol version 4; IPv6: Internet Protocol version 6. If not specified,
        the protocol family will be automatically determined from the address. (One of [‘IPv4’, ‘IPv6’])
        :type protocolFamily: string

        :param name: [THIS IS NOT DOCUMENTED] Name of addrPort section
        :type name: string
        :return: list
        """
        self.host = _Attribute(name='host', value=host)
        self.port = _Attribute(name='port', value=port)
        self.protocolFamily = _Attribute(name='protocolFamily', value=protocolFamily)
        self.name = _Attribute(name='name', value=name)


class connectionRole(_Section):
    """
    Attribute for the role of a connection.
    Used by: listener, connector.
    """
    section_name = 'connectionRole'
    used_by = ['listener', 'connector']

    def __init__(self, role=None, cost=None, name=None):
        """
        :param role: The role of an established connection. In the normal role, the connection is assumed to be used for
        AMQP clients that are doing normal message delivery over the connection. In the inter-router role, the connection
        is assumed to be to another router in the network. Inter-router discovery and routing protocols can only be used
        over inter-router connections. route-container role can be used for router-container connections, for example,
        a router-broker connection. on-demand role has been deprecated.
        (One of [‘normal’, ‘inter-router’, ‘route-container’, ‘on-demand’], default=’normal’)
        :type role: string

        :param cost: For the ‘inter-router’ role only. This value assigns a cost metric to the inter-router connection.
        The default (and minimum) value is one. Higher values represent higher costs. The cost is used to influence the
        routing algorithm as it attempts to use the path with the lowest total cost from ingress to egress. (default=‘1’)
        :type cost: string

        :param name: [THIS IS NOT DOCUMENTED] Name of connectionTole section
        :type name: string

        :return:
        """

        self.role = _Attribute(name='role', value=role)
        self.cost = _Attribute(name='cost', value=cost)
        self.name = _Attribute(name='name', value=name)


class sslProfile(_Section):
    """
    Attributes for setting TLS/SSL configuration for connections.
    Used by: listener, connector.
    """

    section_name = 'sslProfile'
    used_by = ['listener', 'connector']

    def __init__(self, certDb=None, certFile=None, keyFile=None, passwordFile=None, password=None, uidFormat=None,
                 displayNameFile=None, name=None):
        """
        :param certDb: The path to the database that contains the public certificates of trusted
        certificate authorities (CA). (path)
        :type certDb: string

        :param certFile: The path to the file containing the PEM-formatted public certificate
        to be used on the local end of any connections using this profile. (path)
        :type certFile: string

        :param keyFile: The path to the file containing the PEM-formatted private key for the above certificate. (path)
        :type keyFile: string

        :param passwordFile: If the above private key is password protected, this is the path to a file containing
        the password that unlocks the certificate key. (path)
        :type passwordFile: string

        :param password: An alternative to storing the password in a file referenced by passwordFile is to supply
        the password right here in the configuration file. This option can be used by supplying the password in
        the ‘password’ option. Don’t use both password and passwordFile in the same profile.
        :type password: string

        :param uidFormat: A list of x509 client certificate fields that will be used to build a string that will uniquely
        identify the client certificate owner. For e.g. a value of ‘cou’ indicates that the uid will consist
        of c - common name concatenated with o - organization-company name concatenated with u - organization unit;
        or a value of ‘o2’ indicates that the uid will consist of o (organization name) concatenated with
        2 (the sha256 fingerprint of the entire certificate) . Allowed values can be any combination of comma separated
        ‘c’( ISO3166 two character country code),
        ‘s’(state or province),
        ‘l’(Locality; generally - city),
        ‘o’(Organization - Company Name),
        ‘u’(Organization Unit - typically certificate type or brand),
        ‘n’(CommonName - typically a user name for client certificates)
        and ‘1’(sha1 certificate fingerprint, as displayed in the fingerprints section when looking at a certificate
        with say a web browser is the hash of the entire certificate) and
        2 (sha256 certificate fingerprint)
        and 5 (sha512 certificate fingerprint).
        :type uidFormat: string

        :param displayNameFile: The path to the file containing the unique id to display name mapping
        :type displayNameFile: string

        :param name: [THIS IS NOT DOCUMENTED] Name of ssl-profile section
        :type name: string

        :return: list
        """

        self.certDb = _Attribute(name='certDb', value=certDb)
        self.certFile = _Attribute(name='certFile', value=certFile)
        self.keyFile = _Attribute(name='keyFile', value=keyFile)
        self.passwordFile = _Attribute(name='passwordFile', value=passwordFile)
        self.password = _Attribute(name='password', value=password)
        self.uidFormat = _Attribute(name='uidFormat', value=uidFormat)
        self.displayNameFile = _Attribute(name='displayNameFile', value=displayNameFile)
        self.name = _Attribute(name='name', value=name)


class router(_Section):
    """
    Tracks peer routers and computes routes to destinations.
    """

    section_name = 'router'

    def __init__(self, id=None, mode=None, helloInterval=None, helloMaxAge=None, raInterval=None, raIntervalFlux=None,
                 remoteLsMaxAge=None, workerThreads=None, debugDump=None, saslConfigPath=None, saslConfigName=None):
        """
        :param id: Router's unique identity.
        :type id: string

        :param mode: In standalone mode, the router operates as a single component.  It does not participate in
        the routing protocol and therefore will not cooperate with other routers.  In  interior mode, the router operates
        in cooperation with other interior routers in an interconnected network.
        (One of ['standalone', 'interior'], default='standalone')
        :type mode: string

        :param helloInterval: Interval in seconds between HELLO messages sent to neighbor routers. (default=1)
        :type helloInterval:

        :param helloMaxAge: Time in seconds after which a neighbor is declared lost if no HELLO is received. (default=3)
        :type helloMaxAge: string

        :param raInterval: Interval in seconds between Router-Advertisements sent to all routers in a stable network.
        (default=30)
        :type raInterval: string

        :param raIntervalFlux: Interval in seconds between Router-Advertisements sent to all routers during topology
        fluctuations. (default=4)
        :type raIntervalFlux: string

        :param remoteLsMaxAge: Time in seconds after which link state is declared stale if no RA is received. (default=60)
        :type remoteLsMaxAge: string

        :param workerThreads: The number of threads that will be created to process message traffic and other application
        work (timers, non-amqp file descriptors, etc.) (default=4)
        :type workerThreads: string

        :param debugDump: A file to dump debugging information that can’t be logged normally. (path)
        :type debugDump: string

        :param saslConfigPath: Absolute path to the SASL configuration file. (path)
        :type saslConfigPath: string

        :param saslConfigName: Name of the SASL configuration. This string + ‘.conf’ is the name of the configuration
        file. (default='qdrouterd')
        :type saslConfigName: string

        :return: list
        """

        self.id = _Attribute(name='id', value=id)
        self.mode = _Attribute(name='mode', value=mode)
        self.helloInterval = _Attribute(name='helloInterval', value=helloInterval)
        self.helloMaxAge = _Attribute(name='helloMaxAge', value=helloMaxAge)
        self.raInterval = _Attribute(name='raInterval', value=raInterval)
        self.raIntervalFlux = _Attribute(name='raIntervalFlux', value=raIntervalFlux)
        self.remoteLsMaxAge = _Attribute(name='remoteLsMaxAge', value=remoteLsMaxAge)
        self.workerThreads = _Attribute(name='workerThreads', value=workerThreads)
        self.debugDump = _Attribute(name='debugDump', value=debugDump)
        self.saslConfigPath = _Attribute(name='saslConfigPath', value=saslConfigPath)
        self.saslConfigName = _Attribute(name='saslConfigName', value=saslConfigName)


class listener(_Section):
    """
    Listens for incoming connections to the router.
    """

    section_name = 'listener'

    def __init__(self, host=None, port=None, protocolFamily=None, role=None, cost=None, certDb=None, certFile=None,
                 keyFile=None, passwordFile=None, password=None, uidFormat=None, displayNameFile=None,
                 saslMechanism=None, authenticatePeer=None, requireEncryption=None, requireSsl=None,
                 trustedCerts=None, maxFrameSize=None, idleTimeoutSeconds=None, stripAnnotations=None,
                 linkCapacity=None, addrPort=None, connectionRole=None, sslProfile=None, name=None):
        """
        :param host: IP address: ipv4 or ipv6 literal or a host name (default=‘127.0.0.1’)
        :type host: string

        :param port: Port number or symbolic service name. (default=’amqp’)
        :type port: string

        :param protocolFamily: [‘IPv4’, ‘IPv6’] IPv4: Internet Protocol version 4; IPv6: Internet Protocol version 6.
        If not specified, the protocol family will be automatically determined from the address. (One of [‘IPv4’, ‘IPv6’])
        :type protocolFamily: string

        :param role: The role of an established connection. In the normal role, the connection is assumed to be used for
        AMQP clients that are doing normal message delivery over the connection. In the inter-router role, the connection
        is assumed to be to another router in the network. Inter-router discovery and routing protocols can only be used
        over inter-router connections. route-container role can be used for router-container connections, for example,
        a router-broker connection. on-demand role has been deprecated.
        (One of [‘normal’, ‘inter-router’, ‘route-container’, ‘on-demand’], default=’normal’)
        :type role: string

        :param cost: For the ‘inter-router’ role only. This value assigns a cost metric to the inter-router connection.
        The default (and minimum) value is one. Higher values represent higher costs. The cost is used to influence
        the routing algorithm as it attempts to use the path with the lowest total cost from ingress to egress.
        (default=‘1’)
        :type cost: string

        :param certDb: The path to the database that contains the public certificates of trusted
        certificate authorities (CA). (path)
        :type certDb: string

        :param certFile: The path to the file containing the PEM-formatted public certificate
        to be used on the local end of any connections using this profile. (path)
        :type certFile: string

        :param keyFile: The path to the file containing the PEM-formatted private key for the above certificate. (path)
        :type keyFile: string

        :param passwordFile: If the above private key is password protected, this is the path to a file containing
        the password that unlocks the certificate key. (path)
        :type passwordFile: string

        :param password: An alternative to storing the password in a file referenced by passwordFile is to supply
        the password right here in the configuration file. This option can be used by supplying the password in
        the ‘password’ option. Don’t use both password and passwordFile in the same profile.
        :type password: string

        :param uidFormat: A list of x509 client certificate fields that will be used to build a string that will uniquely
        identify the client certificate owner. For e.g. a value of ‘cou’ indicates that the uid will consist
        of c - common name concatenated with o - organization-company name concatenated with u - organization unit;
        or a value of ‘o2’ indicates that the uid will consist of o (organization name) concatenated with
        2 (the sha256 fingerprint of the entire certificate) . Allowed values can be any combination of comma separated
        ‘c’( ISO3166 two character country code),
        ‘s’(state or province),
        ‘l’(Locality; generally - city),
        ‘o’(Organization - Company Name),
        ‘u’(Organization Unit - typically certificate type or brand),
        ‘n’(CommonName - typically a user name for client certificates)
        and ‘1’(sha1 certificate fingerprint, as displayed in the fingerprints section when looking at a certificate
        with say a web browser is the hash of the entire certificate) and
        2 (sha256 certificate fingerprint)
        and 5 (sha512 certificate fingerprint).
        :type uidFormat: string

        :param displayNameFile: The path to the file containing the unique id to display name mapping
        :type displayNameFile: string

        :param saslMechanism: Comma separated list of accepted SASL authentication mechanisms.
        :type saslMechanism: string

        :param authenticatePeer: yes: Require the peer’s identity to be authenticated;
        no: Do not require any authentication.
        :type authenticatePeer: string

        :param requireEncryption:  yes: Require the connection to the peer to be encrypted;
        no: Permit non-encrypted communication with the peer
        :type requireEncryption: string

        :param requireSsl: yes: Require the use of SSL or TLS on the connection;
        no: Allow clients to connect without SSL or TLS.
        :type requireSsl: string

        :param trustedCerts: This optional setting can be used to reduce the set of available CAs for client
        authentication. If used, this setting must provide a path to a PEM file that contains the trusted certificates.
        (path)
        :type trustedCerts: string

        :param maxFrameSize: Defaults to 16384. If specified, it is the maximum frame size in octets that will be used in
        the connection-open negotiation with a connected peer. The frame size is the largest contiguous set of
        uninterrupted data that can be sent for a message delivery over the connection. Interleaving of messages on
        different links is done at frame granularity. (default=16384)
        :type maxFrameSize: string

        :param idleTimeoutSeconds: The idle timeout, in seconds, for connections through this listener. If no frames are
        received on the connection for this time interval, the connection shall be closed. (defaults=16)
        :type idleTimeoutSeconds: string

        :param stripAnnotations: [‘in’, ‘out’, ‘both’, ‘no’] in: Strip the dispatch router specific annotations only
        on ingress; out: Strip the dispatch router specific annotations only on egress; both: Strip the dispatch router
        specific annotations on both ingress and egress; no - do not strip dispatch router specific annotations
        (One of [‘in’, ‘out’, ‘both’, ‘no’], default=’both’)
        :type stripAnnotations: string

        :param linkCapacity: The capacity of links within this connection, in terms of message deliveries. The capacity
        is the number of messages that can be in-flight concurrently for each link.
        :type linkCapacity: string

        :param addrPort: [THIS IS NOT DOCUMENTED] name of addrPort section
        :type addrPort: string

        :param connectionRole: [THIS IS NOT DOCUMENTED] name of connectionRole section
        :type connectionRole: string

        :param sslProfile: [THIS IS NOT DOCUMENTED] name of sslProfile section
        :type sslProfile: string

        :param name: [THIS IS NOT DOCUMENTED] name this listener section
        :type name: string

        :return: list
        """

        self.host = _Attribute(name='host', value=host)
        self.port = _Attribute(name='port', value=port)
        self.protocolFamily = _Attribute(name='protocolFamily', value=protocolFamily)
        self.role = _Attribute(name='role', value=role)
        self.cost = _Attribute(name='cost', value=cost)
        self.certDb = _Attribute(name='certDb', value=certDb)
        self.certFile = _Attribute(name='certFile', value=certFile)
        self.keyFile = _Attribute(name='keyFile', value=keyFile)
        self.passwordFile = _Attribute(name='passwordFile', value=passwordFile)
        self.password = _Attribute(name='password', value=password)
        self.uidFormat = _Attribute(name='uidFormat', value=uidFormat)
        self.displayNameFile = _Attribute(name='displayNameFile', value=displayNameFile)
        self.saslMechanism = _Attribute(name='saslMechanism', value=saslMechanism)
        self.authenticatePeer = _Attribute(name='authenticatePeer', value=authenticatePeer)
        self.requireEncryption = _Attribute(name='requireEncryption', value=requireEncryption)
        self.requireSsl = _Attribute(name='requireSsl', value=requireSsl)
        self.trustedCerts = _Attribute(name='trustedCerts', value=trustedCerts)
        self.maxFrameSize = _Attribute(name='maxFrameSize', value=maxFrameSize)
        self.idleTimeoutSeconds = _Attribute(name='idleTimeoutSeconds', value=idleTimeoutSeconds)
        self.stripAnnotations = _Attribute(name='stripAnnotations', value=stripAnnotations)
        self.linkCapacity = _Attribute(name='linkCapacity', value=linkCapacity)
        self.addrPort = _Attribute(name='addrPort', value=addrPort)
        self.connectionRole = _Attribute(name='connectionRole', value=connectionRole)
        self.sslProfile = _Attribute(name='sslProfile', value=sslProfile)
        self.name = _Attribute(name='name', value=name)


class connector(_Section):
    """
    Establishes an outgoing connection from the router.
    """

    section_name = 'connector'

    def __init__(self, host=None, port=None, protocolFamily=None, role=None, cost=None, certDb=None, certFile=None,
                 keyFile=None, passwordFile=None, password=None, uidFormat=None, displayNameFile=None,
                 saslMechanisms=None, allowRedirect=None, maxFrameSize=None, idleTimeoutSeconds=None,
                 stripAnnotations=None, linkCapacity=None, verifyHostName=None, saslUsername=None, saslPassword=None,
                 addrPort=None, connectionRole=None, sslProfile=None, name=None):
        """
        :param host: IP address: ipv4 or ipv6 literal or a host name
        :type host: string

        :param port: Port number or symbolic service name.
        :type port: string

        :param protocolFamily: [‘IPv4’, ‘IPv6’] IPv4: Internet Protocol version 4; IPv6: Internet Protocol version 6.
        If not specified, the protocol family will be automatically determined from the address.
        :type protocolFamily: string

        :param role: The role of an established connection. In the normal role, the connection is assumed to be used for
        AMQP clients that are doing normal message delivery over the connection. In the inter-router role, the connection
        is assumed to be to another router in the network. Inter-router discovery and routing protocols can only be used
        over inter-router connections. route-container role can be used for router-container connections, for example,
        a router-broker connection. on-demand role has been deprecated.
        :type role: string

        :param cost: For the ‘inter-router’ role only. This value assigns a cost metric to the inter-router connection.
        The default (and minimum) value is one. Higher values represent higher costs. The cost is used to influence
        the routing algorithm as it attempts to use the path with the lowest total cost from ingress to egress.
        :type cost: string

        :param certDb: The path to the database that contains the public certificates of trusted
        certificate authorities (CA). (path)
        :type certDb: string

        :param certFile: The path to the file containing the PEM-formatted public certificate to be used on the local end
        of any connections using this profile. (path)
        :type  certFile: string

        :param keyFile: The path to the file containing the PEM-formatted private key for the above certificate. (path)
        :type keyFile: string

        :param passwordFile: If the above private key is password protected, this is the path to a file containing
        the password that unlocks the certificate key. (path)
        :type passwordFile: string

        :param password: An alternative to storing the password in a file referenced by passwordFile is to supply
        the password right here in the configuration file. This option can be used by supplying the password in the
        ‘password’ option. Don’t use both password and passwordFile in the same profile.
        :type password: string

        :param uidFormat: A list of x509 client certificate fields that will be used to build a string that will uniquely
        identify the client certificate owner. For e.g. a value of ‘cou’ indicates that the uid will consist of
        c - common name concatenated with
        o - organization-company name concatenated with
        u - organization unit;
        or a value of ‘o2’ indicates that the uid will consist of o (organization name)
        concatenated with 2 (the sha256 fingerprint of the entire certificate) .
        Allowed values can be any combination of comma separated
        ‘c’( ISO3166 two character country code),
        ‘s’(state or province),
        ‘l’(Locality; generally - city),
        ‘o’(Organization - Company Name),
        ‘u’(Organization Unit - typically certificate type or brand),
        ‘n’(CommonName - typically a user name for client certificates)
        and ‘1’(sha1 certificate fingerprint, as displayed in the fingerprints section when looking at a certificate with
        say a web browser is the hash of the entire certificate)
        and 2 (sha256 certificate fingerprint) and 5 (sha512 certificate fingerprint).
        :type uidFormat: string

        :param displayNameFile: The path to the file containing the unique id to display name mapping
        :type displayNameFile: string

        :param saslMechanisms: Comma separated list of accepted SASL authentication mechanisms.
        :type saslMechanisms: string

        :param allowRedirect: Allow the peer to redirect this connection to another address. (default=yes)
        :type allowRedirect: string

        :param maxFrameSize: Maximum frame size in octets that will be used in the connection-open negotiation with
        a connected peer. The frame size is the largest contiguous set of uninterrupted data that can be sent for a
        message delivery over the connection. Interleaving of messages on different links is done at frame granularity.
        (default=65536)
        :type maxFrameSize: string

        :param idleTimeoutSeconds: The idle timeout, in seconds, for connections through this connector.
        If no frames are received on the connection for this time interval, the connection shall be closed. (default=16)
        :type idleTimeoutSeconds: string

        :param stripAnnotations: [‘in’, ‘out’, ‘both’, ‘no’] in: Strip the dispatch router specific annotations only on
        ingress; out: Strip the dispatch router specific annotations only on egress; both: Strip the dispatch router
        specific annotations on both ingress and egress; no - do not strip dispatch router specific annotations
        (default=’both’)
        :type stripAnnotations: string

        :param linkCapacity: The capacity of links within this connection, in terms of message deliveries.
        The capacity is the number of messages that can be in-flight concurrently for each link.
        :type linkCapacity: string

        :param verifyHostName: yes: Ensures that when initiating a connection (as a client) the host name in the URL
        to which this connector connects to matches the host name in the digital certificate that the peer sends back
        as part of the SSL connection; no: Does not perform host name verification
        :type verifyHostName: string

        :param saslUsername: The user name that the connector is using to connect to a peer.
        :type saslUsername: string

        :param saslPassword: The password that the connector is using to connect to a peer.
        :type saslPassword: string

        :param addrPort: [THIS IS NOT DOCUMENTED] name of addrPort section
        :type addrPort: string

        :param connectionRole: [THIS IS NOT DOCUMENTED] name of connectionRole section
        :type connectionRole: string

        :param sslProfile: [THIS IS NOT DOCUMENTED] name of sslProfile section
        :type sslProfile: string

        :param name: [THIS IS NOT DOCUMENTED] name this connector section
        :type name: string

        :return: list
        """

        self.host = _Attribute(name='host', value=host)
        self.port = _Attribute(name='port', value=port)
        self.protocolFamily = _Attribute(name='protocolFamily', value=protocolFamily)
        self.role = _Attribute(name='role', value=role)
        self.cost = _Attribute(name='cost', value=cost)
        self.certDb = _Attribute(name='certDb', value=certDb)
        self.certFile = _Attribute(name='certFile', value=certFile)
        self.keyFile = _Attribute(name='keyFile', value=keyFile)
        self.passwordFile = _Attribute(name='passwordFile', value=passwordFile)
        self.password = _Attribute(name='password', value=password)
        self.uidFormat = _Attribute(name='uidFormat', value=uidFormat)
        self.displayNameFile = _Attribute(name='displayNameFile', value=displayNameFile)
        self.saslMechanisms = _Attribute(name='saslMechanisms', value=saslMechanisms)
        self.allowRedirect = _Attribute(name='allowRedirect', value=allowRedirect)
        self.maxFrameSize = _Attribute(name='maxFrameSize', value=maxFrameSize)
        self.idleTimeoutSeconds = _Attribute(name='idleTimeoutSeconds', value=idleTimeoutSeconds)
        self.stripAnnotations = _Attribute(name='stripAnnotations', value=stripAnnotations)
        self.linkCapacity = _Attribute(name='linkCapacity', value=linkCapacity)
        self.verifyHostName = _Attribute(name='verifyHostName', value=verifyHostName)
        self.saslUsername = _Attribute(name='saslUsername', value=saslUsername)
        self.saslPassword = _Attribute(name='saslPassword', value=saslPassword)
        self.addrPort = _Attribute(name='addrPort', value=addrPort)
        self.connectionRole = _Attribute(name='connectionRole', value=connectionRole)
        self.sslProfile = _Attribute(name='sslProfile', value=sslProfile)
        self.name = _Attribute(name='name', value=name)


class log(_Section):
    """
    Configure logging for a particular module. You can use the UPDATE operation to change
    log settings while the router is running.
    """

    section_name = 'log'

    def __init__(self, module=None, enable=None, timestamp=None, source=None, output=None):
        """
        :param module: (One of [‘ROUTER’, ‘ROUTER_CORE’, ‘ROUTER_HELLO’, ‘ROUTER_LS’, ‘ROUTER_MA’, ‘MESSAGE’, ‘SERVER’,
        ‘AGENT’, ‘CONTAINER’, ‘CONFIG’, ‘ERROR’, ‘DISPATCH’, ‘POLICY’, ‘DEFAULT’], required)
        Module to configure. The special module ‘DEFAULT’ specifies defaults for all modules.
        :type module: string

        :param enable: Levels are: trace, debug, info, notice, warning, error, critical. The enable string is
        a comma-separated list of levels. A level may have a trailing ‘+’ to enable that level and above.
        For example ‘trace,debug,warning+’ means enable trace, debug, warning, error and critical. The value ‘none’ means
        disable logging for the module. The value ‘default’ means use the value from the DEFAULT module.
        (default=’default’, required)
        :type enable: string

        :param timestamp: Include timestamp in log messages.
        :type timestamp: string

        :param source: Include source file and line number in log messages.
        :type source: string

        :param output: Where to send log messages. Can be ‘stderr’, ‘syslog’ or a file name.
        :type output: string

        :return: list
        """

        self.module = _Attribute(name='module', value=module)
        self.enable = _Attribute(name='enable', value=enable)
        self.timestamp = _Attribute(name='timestamp', value=timestamp)
        self.source = _Attribute(name='source', value=source)
        self.output = _Attribute(name='output', value=output)


class address(_Section):
    """
    Entity type for address configuration. This is used to configure the treatment of message-routed deliveries
    within a particular address-space. The configuration controls distribution and address phasing.
    """

    section_name = 'address'

    def __init__(self, prefix=None, distribution=None, waypoint=None, ingressPhase=None, egressPhase=None):
        """
        :param prefix: The address prefix for the configured settings  (required)
        :type prefix: string

        :param distribution: Treatment of traffic associated with the address
        (One of [‘multicast’, ‘closest’, ‘balanced’], default=’balanced’)
        :type distribution: string

        :param waypoint: Designates this address space as being used for waypoints. This will cause the proper
        address-phasing to be used.
        :type waypoint: string

        :param ingressPhase: Advanced - Override the ingress phase for this address
        :type ingressPhase: string

        :param egressPhase: Advanced - Override the egress phase for this address
        :type egressPhase: string

        :return: list
        """
        self.prefix = _Attribute(name='prefix', value=prefix)
        self.distribution = _Attribute(name='distribution', value=distribution)
        self.waypoint = _Attribute(name='waypoint', value=waypoint)
        self.ingressPhase = _Attribute(name='ingressPhase', value=ingressPhase)
        self.egressPhase = _Attribute(name='egressPhase', value=egressPhase)


class linkRoute(_Section):
    """
    Entity type for link-route configuration. This is used to identify remote containers that shall be destinations
    for routed link-attaches. The link-routing configuration applies to an addressing space defined by a prefix.
    """

    section_name = 'linkRoute'

    def __init__(self, prefix=None, containerId=None, connection=None, distribution=None, dir=None):
        """
        :param prefix: The address prefix for the configured settings
        :param containerId: ContainerID for the target container
        :param connection: The name from a connector or listener
        :param distribution: Treatment of traffic associated with the address
        (One of [‘linkBalanced’], default=’linkBalanced’)
        :param dir: The permitted direction of links: ‘in’ means client senders; ‘out’ means client receivers
        (One of [‘in’, ‘out’], required)
        :return:
        """

        self.prefix = _Attribute(name='prefix', value=prefix)
        self.containerId = _Attribute(name='containerId', value=containerId)
        self.connection = _Attribute(name='connection', value=connection)
        self.distribution = _Attribute(name='distribution', value=distribution)
        self.dir = _Attribute(name='dir', value=dir)


class autoLink(_Section):
    """
    Entity type for configuring auto-links. Auto-links are links whose lifecycle is managed by the router.
    These are typically used to attach to waypoints on remote containers (clients, etc.).
    """

    section_name = 'autoLink'

    def __init__(self, addr=None, dir=None, phase=None, containerId=None, connection=None):
        """
        :param addr: The address of the provisioned object
        :type addr: string

        :param dir: The direction of the link to be created. In means into the router, out means out of the router.
        :type dir: string

        :param phase: The address phase for this link. Defaults to ‘0’ for ‘out’ links and ‘1’ for ‘in’ links.
        :type phase: string

        :param containerId: ContainerID for the target container
        :type containerId: string

        :param connection: The name from a connector or listener
        :type connection: string

        :return: list
        """

        self.addr = _Attribute(name='addr', value=addr)
        self.dir = _Attribute(name='dir', value=dir)
        self.phase = _Attribute(name='phase', value=phase)
        self.containerId = _Attribute(name='containerId', value=containerId)
        self.connection = _Attribute(name='connection', value=connection)


class policy(_Section):
    """
    Defines global connection limit
    """

    section_name = 'policy'

    def __init__(self, maximumConnections=None, enableAccessRules=None, policyFolder=None, defaultApplication=None,
                 defaultApplicationEnabled=None):
        """
        :param maximumConnections:  Global maximum number of concurrent client connections allowed. Zero implies no limit.
        This limit is always enforced even if no other policy settings have been defined.
        :type maximumConnections: string

        :param enableAccessRules: Enable user rule set processing and connection denial.
        :type enableAccessRules: string

        :param policyFolder: The path to a folder that holds policyRuleset definition .json files. For a small system the
        rulesets may all be defined in this file. At a larger scale it is better to have the policy files in their own
        folder and to have none of the rulesets defined here. All rulesets in all .json files in this folder are
        processed.
        :type policyFolder: string

        :param defaultApplication: Application policyRuleset to use for connections with no open.hostname or a hostname
        that does not match any existing policy. For users that don’t wish to use open.hostname or any multi-tennancy
        feature, this default policy can be the only policy in effect for the network.
        :type defaultApplication: string

        :param defaultApplicationEnabled:  Enable defaultApplication policy fallback logic.
        :type defaultApplicationEnabled: string

        :return:
        """

        self.maximumConnections = _Attribute(name='maximumConnections', value=maximumConnections)
        self.enableAccessRules = _Attribute(name='enableAccessRules', value=enableAccessRules)
        self.policyFolder = _Attribute(name='policyFolder', value=policyFolder)
        self.defaultApplication = _Attribute(name='defaultApplication', value=defaultApplication)
        self.defaultApplicationEnabled = _Attribute(name='defaultApplicationEnabled', value=defaultApplicationEnabled)


class policyRuleset(_Section):
    """
    Per application definition of the locations from which users may connect and the groups to which users belong.
    """

    section_name = 'policyRuleset'

    def __init__(self, maxConnections=None, maxConnPerUser=None, maxConnPerHost=None, userGroups=None,
                 ingressHostGroups=None, ingressPolicies=None, connectionAllowDefault=None, settings=None):
        """
        :param maxConnections: Maximum number of concurrent client connections allowed. Zero implies no limit.
        :param maxConnPerUser: Maximum number of concurrent client connections allowed for any single user.
        Zero implies no limit.
        :param maxConnPerHost: Maximum number of concurrent client connections allowed for any remote host.
        Zero implies no limit.
        :param userGroups: A map where each key is a user group name and the corresponding value is a CSV string naming
        the users in that group. Users who are assigned to one or more groups are deemed ‘restricted’. Restricted users
        are subject to connection ingress policy and are assigned policy settings based on the assigned user groups.
        Unrestricted users may be allowed or denied. If unrestricted users are allowed to connect then they are assigned
        to user group default.
        :param ingressHostGroups: A map where each key is an ingress host group name and the corresponding value is
        a CSV string naming the IP addresses or address ranges in that group. IP addresses may be FQDN strings or numeric
        IPv4 or IPv6 host addresses. A host range is two host addresses of the same address family separated with
        a hyphen. The wildcard host address ‘*’ represents any host address.
        :param ingressPolicies: A map where each key is a user group name and the corresponding value is a CSV string
        naming the ingress host group names that restrict the ingress host for the user group. Users who are members of
        the user group are allowed to connect only from a host in one of the named ingress host groups.
        :param connectionAllowDefault: Unrestricted users, those who are not members of a defined user group, are allowed
        to connect to this application. Unrestricted users are assigned to the ‘default’ user group and receive
        ‘default’ settings.
        :param settings: A map where each key is a user group name and the value is a map of the corresponding settings
        for that group.
        :return: list
        """

        self.maxConnections = _Attribute(name='maxConnections', value=maxConnections)
        self.maxConnPerUser = _Attribute(name='maxConnPerUser', value=maxConnPerUser)
        self.maxConnPerHost = _Attribute(name='maxConnPerHost', value=maxConnPerHost)
        self.userGroups = _Attribute(name='userGroups', value=userGroups)
        self.ingressHostGroups = _Attribute(name='ingressHostGroups', value=ingressHostGroups)
        self.ingressPolicies = _Attribute(name='ingressPolicies', value=ingressPolicies)
        self.connectionAllowDefault = _Attribute(name='connectionAllowDefault', value=connectionAllowDefault)
        self.settings = _Attribute(name='settings', value=settings)
