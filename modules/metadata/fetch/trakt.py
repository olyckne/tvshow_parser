from ..metadata import *
import json
import datetime


class Trakt(Metadata):

    baseUrl = "http://api.trakt.tv/"
    url = {
        "episode": baseUrl + "show/episode/summary.json/",
        "season": baseUrl + "show/seasons.json/",
        "watchlist": baseUrl + "show/episode/watchlist/",
        "movie": baseUrl + "movie/summary.json/"
    }

    def __init__(self, config):
        if not "trakt" in config:
            raise Exception("Need trakt config key, username sha1 of password")

        self.trakt = config['trakt']
        super(Trakt, self).__init__(config)

    def getInfo(self, data):
        if self.config['type'] == "TV":
            return self.getEpisodeInfo(data)
        elif self.config['type'] == "MOVIE":
            return self.getMovieInfo(data)

    def getEpisodeInfo(self, name, season=0, episode=0, hd=False):
        if isinstance(name, dict) or isinstance(name, list):
            season = name['season'] if "season" in name else name[1]
            episode = name['episode'] if "episode" in name else name[2]
            name = name['name'] if "name" in name else name[0]
            hd = name['hd'] if 'hd' in name else False

        serie = {
            "name": name,
            "season": season,
            "episode": episode,
            "hd": hd
        }

        url = self.constructUrl("episode", [name, season, episode])
        resp, content = self.httprequest(url, "GET")
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
            resp, content = self.httprequest(url, "GET")
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

    def getMovieInfo(self, name):
        url = self.constructUrl("movie", [name])
        print url

    def getArtwork(self, serie, season):
        name = serie['name'] if "name" in serie else serie
        url = self.constructUrl("season", [name, season])
        print url
        image = False
        resp, content = self.httprequest(url, "GET")
        content = json.loads(content)
        if not "status" in content:
            for s in content:
                if int(s['season']) == int(season):
                    image = s['images']['poster']

        if image:
            resp, content = self.httprequest(image, "GET")
            if "status" in resp and resp['status'] == '200':
                print "downloading artwork"
                with open("art.jpg", "wb") as f:
                    f.write(content)


    def constructUrl(self, type, params):
        url = self.url[type] + self.trakt['key'] + "/"
        for param in params:
            url += param + "/"

        return url.replace(" ", "-")
