from messaging_components.config.config import Config


class DispatchConfig(Config):

    def __init__(self, **kwargs):
        super(DispatchConfig, self).__init__(**kwargs)

    def apply_config(self, configuration):
        pass

    def create_default_configuration(self, **kwargs):
        pass

    def create_configuration(self, config_file_path):
        self.load_configuration_yaml(config_file_path)

    def load_configuration(self):
        pass
