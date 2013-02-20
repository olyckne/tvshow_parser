from metadata import *
import httplib2
import json
import datetime


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

    def getEpisodeInfo(self, name, season, episode):
    def getInfo(self, data):
        if self.config['type'] == "TV":
            return self.getEpisodeInfo(data)
        elif self.config['type'] == "MOVIE":
            pass
        serie = {
            "name": name,
            "season": season,
            "episode": episode
        }

        url = self.constructUrl("episode", [name, season, episode])
        cacheDir = self.config['temp']['path'] + "/.cache" if "temp" in self.config else ".cache"
        h = httplib2.Http(cacheDir)
        resp, content = h.request(url, "GET")
        content = json.loads(content)
        if not "status" in content:
            show = content['show']
            episode = content['episode']
            serie['poster'] = show['images']['poster']
            serie['desc'] = episode['overview'].replace('"', "'")
            serie['epName'] = episode['title'].replace('"', "'")
            serie['year'] = datetime.date.fromtimestamp(episode['first_aired']).isoformat()
            genres = show['genres']
            serie['genre'] = genres[0]
            genres.pop(0)

            serie['comments'] = ", ".join(genres)
            serie['id'] = episode['tvdb_id']

            url = self.constructUrl("season", [name])
            resp, content = h.request(url, "GET")
            content = json.loads(content)

            if not "status" in content:
                for s in content:
                    if int(serie['season']) == int(s['season']):
                        serie['nrOfEpisodes'] = s['episodes']
                        break
        else:
            print "no data"
        print url

        return serie

    def getArtwork(self, serie, season):
        name = serie['name'] if "name" in serie else serie
        url = self.constructUrl("season", [name, season])
        print url
        image = False
        cacheDir = self.config['temp']['path'] + "/.cache" if "temp" in self.config else ".cache"
        h = httplib2.Http(cacheDir)
        resp, content = h.request(url, "GET")
        content = json.loads(content)
        if not "status" in content:
            for s in content:
                if int(s['season']) == int(season):
                    image = s['images']['poster']

        if image:
            resp, content = h.request(image, "GET")
            if "status" in resp and resp['status'] == '200':
                print "downloading artwork"
                with open("art.jpg", "wb") as f:
                    f.write(content)

    def constructUrl(self, type, params):
        url = self.url[type] + self.trakt['key'] + "/"
        for param in params:
            url += param + "/"

        return url.replace(" ", "-")
