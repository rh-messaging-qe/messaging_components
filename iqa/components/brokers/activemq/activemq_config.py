from iqa.components.brokers.broker_config import BrokerConfiguration


class ActiveMQConfig(BrokerConfiguration):

    def __init__(self, **kwargs):
        super(ActiveMQConfig).__init__(**kwargs)
