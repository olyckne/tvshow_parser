import abc


class Notification(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def sendNotification(self):
        pass
