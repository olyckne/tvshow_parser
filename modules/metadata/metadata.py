import abc


class Metadata(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def getEpisodeInfo(self, serie, season, episode):
        return False

    @abc.abstractmethod
    def getArtwork(self, serie, season):
        return False
