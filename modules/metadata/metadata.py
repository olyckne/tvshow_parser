import httplib2


class Metadata(object):

    def __init__(self, config):
        self.config = config

    def getEpisodeInfo(self, serie, season, episode):
        return False

    def getArtwork(self, serie, season):
        return False

    def httprequest(self, url, type="GET", data={}):
        cacheDir = self.config['temp']['path'] + "/.cache" if "temp" in self.config else ".cache"
        h = httplib2.Http(cacheDir)

        return h.request(url, type)
