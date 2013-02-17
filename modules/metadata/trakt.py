from metadata import *


class Trakt(Metadata):

    baseUrl = "http://api.trakt.tv/"
    url = {
        "episode": baseUrl + "show/episode/summary.json/",
        "season": baseUrl + "show/seasons.json/",
        "watchlist": baseUrl + "show/episode/watchlist/"
    }

    def __init__(self, config):
        if not "trakt" in config:
            raise Exception("Need trakt config key, username sha1 of password")

        self.trakt = config['trakt']
        super(Trakt, self).__init__(config)

    def getEpisodeInfo(self, serie, season, episode):
        pass

    def getArtwork(serie, season):
        pass
