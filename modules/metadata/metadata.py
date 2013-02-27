import abc
import httplib2


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

    def httprequest(self, url, type="GET", data={}):
        cacheDir = self.config['temp']['path'] + "/.cache" if "temp" in self.config else ".cache"
        h = httplib2.Http(cacheDir)

        return h.request(url, type)
