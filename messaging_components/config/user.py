
class User(object):

    def __init__(self, username, password, **kwargs):
        self.username = username
        self.password = password
        self.kwargs = kwargs
        self.roles = []

        if self.kwargs.get('roles') is not None:
            self.roles = self.kwargs.get('roles')
