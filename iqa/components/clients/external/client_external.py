from messaging_abstract.component import Client, Node, Executor
from messaging_components.clients.external.command.client_command import ClientCommand


class ClientExternal(Client):
    """
    Represents abstract clients that are executed externally as command line applications.
    """

    # Default is run forever
    # As mixing --timeout with --count is causing issues
    TIMEOUT = 90

    def __init__(self, name: str, node: Node, executor: Executor, **kwargs):
        super(ClientExternal, self).__init__(name, node, executor, **kwargs)
        self.execution = None  # type: Execution
        self._command = None  # type: ClientCommand
        self._url = None  # type: str
        self.reset_command()

        # initializing client from kwargs
        for func in [self.set_url, self.set_auth_mechs, self.set_ssl_auth]:
            self.call_if_all_arguments_in_kwargs(func, **kwargs)

    @property
    def command(self) -> ClientCommand:
        return self._command

    def reset_command(self):
        """
        Creates a new command instance based on concrete implementation.
        :return:
        """
        self._command = self._new_command(stdout=True, timeout=ClientExternal.TIMEOUT,
                                          daemon=True)  # type: ClientCommand

    def get_url(self):
        return self._url

    def set_url(self, url: str):
        """
        Saves url property internally and invoke concrete _set_url implementation
        which is responsible for properly using it according to each external client needs.
        :param url:
        :return:
        """
        self._set_url(url)

    def _new_command(self, stdout: bool=False, stderr: bool=False,
                daemon: bool=False, timeout: int=0,
                encoding: str="utf-8") -> ClientCommand:
        """
        Must return a ClientCommand implementation for the command that is related
        with the concrete client.
        :param stdout:
        :param stderr:
        :param daemon:
        :param timeout:
        :param encoding:
        :return:
        """
        raise NotImplementedError

    def _set_url(self, url: str):
        """
        This method must be implemented by each concrete client by adjusting url parts
        into appropriate command elements, in order to execute it correctly.
        :param url:
        :return:
        """
        raise NotImplementedError

    def set_auth_mechs(self, mechs: str):
        """
        Implementing clients must know how to adjust mechanisms (if supported).
        :param mechs:
        :return:
        """
        raise NotImplementedError

    def set_ssl_auth(self, pem_file: str=None, key_file: str=None, keystore: str=None,
                     keystore_pass: str=None, keystore_alias: str=None):
        """
        Allows implementing clients to use the SSL credentials according to each implementing model.
        :param pem_file:
        :param key_file:
        :param keystore:
        :param keystore_pass:
        :param keystore_alias:
        :return:
        """
        raise NotImplementedError
