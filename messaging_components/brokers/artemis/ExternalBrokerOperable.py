import logging
import posixpath

import time

from datetime import datetime

from messaging_components.brokers.artemis import Utils
from messaging_components.brokers.artemis.ExternalBroker import ExternalBroker

LOGGER = logging.getLogger(__name__)


class ExternalBrokerOperable(ExternalBroker):
    """ Operable External broker class, which supports
    - gathering configuration data from input file
    - operations of this external broker (start, stop, status)

    Note: Custom configuration change on the fly is not supported.
    """

    def start(self, in_exp_result=True, as_service=True, wait_for_accessible=False):
        """Start operable broker object as service or as foreground process.
        Possibly wait for accessible broker state (via jolokia/Started call).

        :param in_exp_result: Expected result of start operation
        :type in_exp_result: bool
        :param as_service: whether to run as service or as foreground process
        :type as_service: bool
        :param wait_for_accessible: whether to wait for broker to start or not
        :type wait_for_accessible: bool
        :return: result of "running" operation or both running & accessible operations
        :rtype: bool
        """
        if as_service:
            cmd = "runuser -l %s %s start" % \
                  (self.opts.get('broker_ruser', 'jamq'),  # TODO(mtoth) platform dependent!
                   self._get_artemis_service_bin())
        else:
            # TODO(mtoth) needed?
            cmd = "runuser -l %s %s run" % \
                  (self.opts.get('broker_ruser', 'jamq'),  # TODO(mtoth) platform dependent!
                   self._get_artemis_bin())

        result = self.get_host().execute(cmd)
        result.wait_for_data()

        # normal daemon setup & run (as non-admin user -> runuser)
        self.test.add_run_and_report(result, in_exp_result)
        self._set_pid()

        if wait_for_accessible:
            retry_result = Utils.retry(self.is_accessible, True, max_count=60, max_duration=120)
            self.test.add_check_and_report("Broker is accessible", retry_result[0])
            return retry_result[0]
        return self.is_running()

    def graceful_stop(self, as_service=True):
        """Gracefully stop this broker as service.

        :param as_service: whether to run as service or as foreground process
        :type as_service: bool
        :return: ecode of stop operation
        :rtype: int
        """
        cmd = "runuser -l %s %s stop" % (self.opts.get('broker_ruser', 'jamq'),
                                         self._get_artemis_service_bin())  # TODO(mtoth) platform dependent!

        result = self.get_host().execute(cmd)
        result.wait_for_data()

        self.test.add_run_and_report(result, True)
        self.pid = None

        return result.ecode

    def stop(self, in_killsig_id=0, in_stop_all_brokers_on_node=False, as_service=True):
        """ stop (one/all) broker (by selectable signal)
        :param in_killsig_id: signal number for kill command
        :type in_killsig_id: int
        :param in_stop_all_brokers_on_node: Invalid not used in this method (inheritance issue)
        :type in_stop_all_brokers_on_node: bool
        :param as_service: whether to run as service or as foreground process
        :type as_service: bool
        :return: ecode of stop command
        :rtype: int
        """

        if in_killsig_id == 0 or in_killsig_id is None:
            return self.graceful_stop(as_service)

        int_pid = self.get_pid()
        # kill the broker
        cmd = "kill -s %s %s" % (in_killsig_id, int_pid)  # TODO(mtoth) platform dependent!
        LOGGER.warn('%s' % cmd)
        result = self.get_host().execute(cmd)
        result.wait_for_data()

        self.test.add_run_and_report(result, True)
        self.pid = None

        return result.ecode

    def status(self, in_update_ena=True):
        """Get current status of this broker.

        :param in_update_ena: Not used here (inheritance issue)
        :type in_update_ena: bool
        :return: If broker is accessible (via jolokia status) return True, False otherwise
        :rtype: bool
        """
        if self.get_pid() is not None:
            LOGGER.warn("Accessible? %s " % self.is_accessible())
            return self.is_accessible()
        else:
            return False

    def get_pid(self, in_update_ena=False):
        """Get a pid number for this broker from <instance>/artemis.pid file.

        :param in_update_ena: Not used here (inheritance issue)
        :type in_update_ena: bool
        :return: pid number of this broker
        :rtype: int
        """
        if self.pid is None:
            return self._set_pid()
        else:
            return self.pid

    def is_running(self, in_update_ena=False):
        """Return a boolean value if broker is running.
        Method does not report its check, because we're not interested
        in warnings and passes of kill -0.
        We just need to know if pid exists or not.

        :param in_update_ena: Not used here (inheritance issue)
        :type in_update_ena: bool
        :return: True if broker has pid (is running) else otherwise
        :rtype: bool
        """
        # return self.get_pid() is not None
        pid = self.get_pid()
        cmd = "kill -s 0 %s" % pid  # TODO(mtoth) platform dependent!
        running_pid_result = self.get_data().get_test_node().execute(cmd)
        running_pid_result.wait_for_data()
        return running_pid_result.ecode == 0

    def _set_pid(self, pid=None):
        """Set pid number of broker from <instance>/artemis.pid file.
        Set 'pid' to this object if provided, figure it out otherwise.

        :param pid: expected broker pid
        :type pid: int
        :return: active pid number or None if unknown
        :rtype: int
        """
        if pid is None:
            artemis_pid_file = posixpath.join(self.get_data().get_instance_data_dir(), "artemis.pid")
            cmd = "cat %s" % artemis_pid_file  # TODO(mtoth) not very platform friendly command
            check_pid_result = self.get_data().get_test_node().execute(cmd)
            check_pid_result.wait_for_data()

            if check_pid_result.stdout:
                self.pid = int(*check_pid_result.stdout)
            else:
                LOGGER.debug("Unable to get process id of broker. Not running?")
                self.pid = None
        else:
            self.pid = pid
        LOGGER.debug("New Artemis pid=%s", self.pid)
        return self.pid

    def _get_artemis_service_bin(self):
        """Get a full path of instance/bin/artemis-service

        :return: full path to instance/bin/artemis-service
        :rtype: str
        """
        # TODO win artemis-service vs artemis-service.exe (?)
        return posixpath.join(self.get_data().get_instance_bin_dir(), "artemis-service")

    def _get_artemis_bin(self):
        """Get a full path to instance/bin/artemis

        :return: full path to instance/artemis
        :rtype: str
        """
        return posixpath.join(self.get_data().get_instance_bin_dir(), "artemis")

    def generate_thread_dump(self, print_thread_dump=False):
        """Generate Thread dump using jstack for this Artemis broker process.

        :param print_thread_dump: whether to print thread dump on stdout or not
        :type print_thread_dump: bool
        :return: path to generated thread dump file
        :rtype: str
        """
        thread_dump_name = 'thread_dump_%s.log' % datetime.now().isoformat()
        thread_dump_path = posixpath.join(self.get_data().get_instance_log_dir(), thread_dump_name
                                  )
        cmd = "runuser -l %s -c 'jstack -l %s | tee %s'" % (
            self.opts.get('broker_ruser', 'jamq'),
            self.get_pid(),
            thread_dump_path)  # TODO(mtoth) platform dependent!
        jstack_result = self.get_data().get_test_node().execute(cmd)
        jstack_result.wait_for_data()

        LOGGER.info('%s thread dump %s' % (self.get_data().get_instance_name(), thread_dump_path))
        if print_thread_dump:
            LOGGER.info(jstack_result.stdout)
        return thread_dump_path

    def __str__(self):
        return self.data.get_instance_name()

    def __repr__(self):
        return self.data.get_instance_name()