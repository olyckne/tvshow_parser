import httplib2
import json
import os


class Metadata(object):

    def __init__(self, config, headers={}):
        self.config = config
        self.headers = headers

    def getEpisodeInfo(self, serie, season, episode):
        return False

    def getArtworkLink(self, serie,season):
        return False

    def getArtwork(self, serie, season):
        return False

    def httprequest(self, url, type="GET", data={}, headers={}):
        if "temp" in self.config:
            cacheDir = os.path.join(self.config['temp']['path'], '.cache')
        else:
            cachedir = os.path.join(self.config['config_root'], '.cache')
        h = httplib2.Http(cacheDir)
        headers = dict(self.headers.items() + headers.items())
        
        return h.request(url, type, body=json.dumps(data), headers=headers)
