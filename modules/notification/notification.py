import abc


class Notification(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def sendNotification(self):
        pass
