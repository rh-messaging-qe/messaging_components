from autologging import logged, traced

import os

from .execution import Execution
from .local_exec import LocalExec


@logged
@traced
class AnsibleCMD:
    """
    Ansible program abstraction
    """

    def __init__(self, inventory):
        """
        :param inventory:
        :type inventory:
        """
        self.inventory = inventory

    @staticmethod
    def cli_cmd(host, module, args):
        """
        Execute command on node by using Ansible.

        :param host:
        :type host:
        :param module:
        :type module:
        :param args:
        :type args:

        :return:
        :rtype:
        """
        if len(args) > 1:
            args = [' '.join(args)]

        # command = ['ansible', host, '-i', inventory, '-m', module, '-a'] + args
        command = ['ansible', host, '-m', module, '-a'] + args
        process = LocalExec(command)
        process.run_and_wait()
        return process

    @staticmethod
    def cli_playbook(playbook, inventory, args):
        """
        Execute command on node by using Ansible.

        :param playbook:
        :type playbook:
        :param inventory:
        :type inventory:
        :param args:
        :type args:

        :return:
        :rtype:
        """
        # Check if Ansible playbook exists
        if not os.path.exists(playbook):
            AnsibleCMD.__log.debug('Wrong playbook: %s' % playbook)

        command = ['ansible-playbook', '-i', inventory, playbook, '-a', '-f', '10'] + args
        process = LocalExec(command)
        process.run_and_wait()
        return process


@logged
@traced
class AnsibleExecution(Execution):
    """
    Ansible CLI Ad-Hoc Commands
    """

    def __init__(self, hostname, ansible_cmd: AnsibleCMD):
        Execution.__init__(self, hostname=hostname)
        self.ansible_cmd = ansible_cmd

    def module(self, module: str, args: []):
        """
        Run ansible module on node.

        :param module:
        :type module:
        :param args:
        :type args:
        :return:
        :rtype:
        """
        AnsibleExecution.__log.info('Run module %s to node %s..' % (module, self.hostname))
        process = self.ansible_cmd.cli_cmd(
            host=self.hostname,
            # inventory=self.ansible_cmd.inventory,
            module=module,
            args=args
        )
        return process

    def _execute(self, command):
        """
        Execute command on node by using Ansible command module.

        :param command:
        :type command:

        :return:
        :rtype:
        """
        process = self.module(
            module='shell',
            args=command
        )
        return process

    def ping(self):
        """
        Run Ansible ping module for ping node.

        :return:
        :rtype:
        """
        AnsibleCMD.__log.info('Pinging node %s..' % self.hostname)
        ping = self.module(
            module='ping',
            args='data=pong'
        )
        ecode = ping.get_ecode()
        result = 'passed' if ecode == 0 else 'failed'
        AnsibleExecution.__log.info('Ping for node %s %s.' % (self.hostname, result))

        return True if ecode == 0 else False


@logged
@traced
class AnsibleAPI(Execution):
    """
    @TODO Ansible API Usage
    """

    def __init__(self, hostname):
        Execution.__init__(self, hostname=hostname)
