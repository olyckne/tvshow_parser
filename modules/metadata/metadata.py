import httplib2
import json


class Metadata(object):

    def __init__(self, config, headers={}):
        self.config = config
        self.headers = headers

    def getEpisodeInfo(self, serie, season, episode):
        return False

    def getArtwork(self, serie, season):
        return False

    def httprequest(self, url, type="GET", data={}, headers={}):
        cacheDir = self.config['temp']['path'] + "/.cache" if "temp" in self.config else ".cache"
        h = httplib2.Http(cacheDir)
        headers = dict(self.headers.items() + headers.items())
        
        return h.request(url, type, body=json.dumps(data), headers=headers)
