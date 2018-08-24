"""
    # TODO jstejska: Package description
"""

from autologging import logged, traced
from iqa_common.executor import Executor
from messaging_abstract.component.client import Client, Node

import messaging_components.protocols as protocols


@logged
@traced
class ClientCore(Client):
    """Internal core Proton mapping client."""

    supported_protocols = [protocols.Amqp10()]
    implementation = 'core'
    version = '0.1'

    def __init__(self, name: str, node: Node, executor: Executor):
        super(ClientCore, self).__init__(name, node, executor)

#
# """
#     # TODO jstejska: Package description
# """
#
# # -*- coding: utf-8 -*-
#
# import threading
#
# from proton.handlers import MessagingHandler
# from proton.reactor import Container
#
#
# class Timeout(object):
#     def __init__(self, handler):
#         self.registrated_handler = handler
#
#     def on_timer_task(self, event):
#         self.registrated_handler.timeout(event)
#
#
# class Client(MessagingHandler):
#     # TODO error handling is not incorporated, this is just a raw idea
#     """Client represents an entity in the framework capable of manipulation with messages (sending, receiving, parsing ...)
#     """
#
#     def __init__(self, blocking=False):
#         """ # TODO jstejska: Description
#
#         :param blocking: if clients blocks program execution - runs on foreground
#         :type blocking: bool
#         """
#         super(Client, self).__init__()
#         self.hostname = None
#         self.address = None
#         self.message_pool = []
#         self.error = False
#         self.container = None
#         self.event = None
#         self.thread = None
#         self._blocking = blocking
#
#     @property
#     def msg_cnt(self):
#         """ # TODO jstejska: Description
#
#         :return: count of available messages
#         :rtype: int
#         """
#         return len(self.message_pool)
#
#     def run(self):
#         """Starts clients.
#
#         Client runs on foreground/background according to its configuration during initialization
#
#         :return: None
#         :rtype: # TODO jstejska: type
#         """
#         self.thread = threading.Thread(target=self.container.run)  # assing a thread
#         if self._blocking:
#             self.thread.run()
#         else:
#             self.thread.start()  # invokes separate thread of control
#
#     def stop(self):
#         self.thread.join(timeout=1)
#
#
# class Sender(Client):
#     """Most basic example clients capable of sending messages."""
#
#     def __init__(self, hostname="localhost", address="test_queue", count=1, messages=None, blocking=False):
#         """ # TODO jstejska: Description
#
#         :param hostname: hostname of the physical node with routers/brokers/receiver
#         :type hostname: str
#         :param address: address where to send (queue name, topic name)
#         :type address: str
#         :param count: count of messages to send - every message from the 'messages' will be sent *count* times
#         :type count: int
#         :param messages: pool of messages to send, note count - proton.Message
#         :type messages: list
#         :param blocking: if clients blocks program execution - runs on foreground
#         :type blocking: bool
#         """
#         super(Sender, self).__init__(blocking=blocking)
#         if messages is None:
#             messages = []
#         self.hostname = hostname
#         self.address = address
#         self.counter = 0
#         self.max_messages = count
#         self.messages = messages
#         self.container = None
#         self.container = Container(self)
#
#     def on_start(self, event):  # event loop starts
#         conn = event.container.connect(self.hostname)
#         event.container.create_sender(conn, self.address)
#
#     def on_sendable(self,
#                     event):  # link has credit and we can transfer messages TODO add link credit checking see dtests
#         if event.sender:
#             for message in self.messages:
#                 counter_per_message = 0
#                 if counter_per_message < self.max_messages:
#                     event.sender.send(message)
#                     self.message_pool.append(message)  # sent messages to the pool
#                     counter_per_message += 1
#                 self.counter += 1
#             if self.counter == self.max_messages:
#                 event.connection.close()
#
#     @staticmethod
#     def on_connection_closed(event):
#         event.container.stop()
#
#
# class Receiver(Client):
#     def __init__(self, hostname="localhost", address="test_queue", expected=1, blocking=True):
#         """ # TODO jstejska: Description
#
#
#         :param hostname: hostname of the physical node with routers/brokers/receiver
#         :type hostname: str
#         :param address: address where to send (queue name, topic name)
#         :type address: str
#         :param expected: expected count of messages to receive
#         :type expected: int
#         :param blocking: if clients blocks program execution - runs on foreground
#         :type blocking: bool
#         """
#         super(Receiver, self).__init__(blocking=blocking)
#         self.hostname = hostname
#         self.confirmed = 0
#         self.total = expected
#         self.received = 0
#         self.receiver = None
#         self.address = address
#         self.container = Container(self)
#         self.timer = None
#
#     def on_reactor_init(self, event):  # called when event loop - the reactor - starts
#         super(Receiver, self).on_reactor_init(event)
#         self.timer = event.reactor.schedule(5, Timeout(
#             self))  # schedule timeout -- good for testing purposes to not hang out
#         self.receiver = event.container.create_receiver(self.hostname + "/" + self.address)
#         self.receiver.open()
#
#     def timeout(self, event):  # TODO error handling is missing
#         self.error = 1
#         if self.receiver is not None:
#             self.receiver.close()
#         event.container.stop()
#
#     def on_message(self, event):  # we got a message
#         if event.receiver:
#             self.message_pool.append(event.message)
#             self.received += 1
#         if self.received == self.total:
#             if self.receiver is not None:
#                 self.receiver.close()
#         event.container.stop()
