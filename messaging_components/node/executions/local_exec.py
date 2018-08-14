# -*- coding: utf-8 -*-
"""
DOC STRING
"""
import logging
import shlex
import subprocess
import tempfile
import time
import xtlog

from autologging import logged, traced

logger = logging.getLogger(__name__)


@logged
@traced
class LocalExec:
    """
    Local process execution

    TODO: Timeout, complete log_adapter
    """

    def __init__(self, cmd, timeout=None, stdin=None):
        """
        Constructor that will not execute anything, just set things up
        """
        self.cmd = cmd
        self.x_cmd = None
        self._process_cmd()
        self.timeout = timeout
        self.shell = False
        self.ecode = None
        self.stdin = stdin
        self.stdout = []
        self.stderr = []
        self.fh_stdin = None
        self.fh_stderr = None
        self.fh_stdout = None
        self.process = None
        self.opts = {}
        self.ts_start = None
        self.ts_stop = None
        self.host = 'localhost'
        self.exec_log_adapter = xtlog.adapters.RemoteExecAdapter(xtlog, {'host': self.host, 'user': None})

    def __remove_tailing_newlines(self):
        """
        remove tailing newline chars from detected stdout/err
        """
        if self.stdout and self.stdout[-1] == '':
            self.stdout.pop(-1)
        if self.stderr and self.stderr[-1] == '':
            self.stderr.pop(-1)

    def _process_cmd(self):
        """
        Post-process command, split to correct arguments
        """
        # pre-process for shlex(posix=True), it consumes '\' as
        # escapes, let's double it
        if not isinstance(self.cmd, list):
            tmp_cmd = self.cmd.replace('\\', '\\\\')
            self.x_cmd = shlex.split(tmp_cmd)
        else:
            self.x_cmd = self.cmd

    def _pre_start(self):
        # assign pipe channel to stdin if stdin given
        if self.stdin:
            self.fh_stdin = tempfile.TemporaryFile()
            self.fh_stdin.write(self.stdin)
            self.fh_stdin.seek(0)

        self.fh_stdout = tempfile.TemporaryFile()
        self.fh_stderr = tempfile.TemporaryFile()

    def _sync_stdx(self):
        if not self.fh_stdout.closed:
            self.fh_stdout.seek(0)
            self.stdout = self.fh_stdout.readlines()
            self.fh_stdout.seek(0, 2)

        if not self.fh_stderr.closed:
            self.fh_stderr.seek(0)
            self.stderr = self.fh_stderr.readlines()
            self.fh_stdout.seek(0, 2)

    def _read_stdx(self):
        self._sync_stdx()
        self.fh_stdout.close()
        self.fh_stderr.close()
        if self.fh_stdin:
            self.fh_stdin.close()

    def start(self):
        """Start pre-prepared command"""
        self._pre_start()

        command = self.x_cmd
        if self.shell:
            command = self.cmd

        # assign start timestamp
        self.ts_start = time.time()

        LocalExec.__log.debug('COMMAND: "%s"' % ' '.join(command))

        # call the process
        self.process = subprocess.Popen(
            command,
            stdin=self.fh_stdin,
            stdout=self.fh_stdout,
            stderr=self.fh_stderr,
            shell=self.shell
        )

        return self.process

    @staticmethod
    def _convert_ecode(ecode):
        if ecode is None:
            return None
        # kill ecodes are marked as negative values of signals (SIGTERM -15)
        if ecode < 0:
            # convert ecode
            ecode = -ecode + 128
        return ecode

    def wait_for_exit(self):
        """
        waits for process to finish
        """
        LocalExec.__log.debug('wait_for_exit(%s)' % self.x_cmd[0])
        try:
            self.process.communicate()
            self.process.wait()
            self.ts_stop = time.time()
            LocalExec.__log.debug("ecode: %s" % self.process.returncode)
            LocalExec.__log.debug("Execution time: %s sec" % self.get_duration())
            self._read_stdx()
        except IOError as exc:
            LocalExec.__log.warning("wait_for_exit(): process error %s" % exc)

        self.ecode = self._convert_ecode(self.process.returncode)
        return self.ecode

    def run_and_wait(self):
        """
        runs and waits for completion, returns exit code or None
        """
        self.start()
        self.wait_for_exit()

        # STDOUT DEBUG
        stdo = self.get_stdout()
        stdo = '\n%s' % '\n'.join(stdo) if stdo else "EMPTY"
        LocalExec.__log.debug('STDOUT: %s' % stdo)

        # STDERR DEBUG
        stde = self.get_stderr()
        stde = '\n%s' % '\n'.join(stde) if stde else "EMPTY"
        LocalExec.__log.debug('STDERR: %s' % stde)

        return self.ecode

    def get_ecode(self):
        """
        returns the process exit code or None if it got killed / did not exit
        """
        if self.ecode is not None:
            return self.ecode
        if self.process is not None:
            return self._convert_ecode(self.process.returncode)
        return None

    def finished(self):
        """
        returns whether process has finished (True / False ~ yes / no)
        """
        if not self.process:
            return True
        return self.process.poll()

    def get_stdout(self):
        """
        returns stdout from the process run
        """
        if not self.finished():
            self._sync_stdx()
        return strip_endlines(self.stdout)

    def get_stderr(self):
        """
        returns stderr from the process run
        """
        if not self.finished():
            self._sync_stdx()
        return strip_endlines(self.stderr)

    def get_stdin(self):
        """
        returns stdin fed to the process
        """
        return self.stdin

    def set_stdin(self, in_str):
        """
        sets stdin stream to be fed to the process
        """
        self.stdin = in_str
        return self.stdin

    def get_duration(self):
        """
        gets duration of runned command or None if command was not launched yet
        """
        if self.ts_start is None:
            return None
        ts_end = self.ts_stop or time.time()

        return ts_end - self.ts_start


def strip_endlines(in_arg):
    """
    remove eol characters Linux/Win/Mac (input can be string or list of strings)
    """

    if isinstance(in_arg, (tuple, list)):
        buff = []
        for x in in_arg:
            if isinstance(x, bytes):
                buff.append(x.rstrip().decode('utf-8'))
            elif isinstance(x, str):
                buff.append(x.rstrip())
            else:
                # input is unknown
                buff.append(in_arg)
        return buff

    elif isinstance(in_arg, bytes):
        return in_arg.rstrip().decode('utf-8')

    elif isinstance(in_arg, str):
        return in_arg.rstrip()
    else:
        # input is unknown
        return in_arg
