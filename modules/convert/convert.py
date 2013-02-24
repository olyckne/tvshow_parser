import abc


class Convert(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def convert(self):
        pass
