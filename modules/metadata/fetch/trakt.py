from ..metadata import *
import json
import datetime
import yaml
import time
import os

class Trakt(Metadata):

    baseUrl = "https://api-v2launch.trakt.tv/"
    url = {
        "token": baseUrl + "oauth/token",
        "episode": baseUrl + "shows/{show}/seasons/{season}/episodes/{episode}?extended=full",
        "seasons": baseUrl + "shows/{show}/seasons?extended=full,images",
        "season": baseUrl + "show/season.json/",
        "watchlist": baseUrl + "show/episode/watchlist/",
        "movie": baseUrl + "movie/summary.json/"
    }

    def __init__(self, config):
        required = ['client_id', 'client_secret', 'redirect_uri', 'pin_url']
        if not 'trakt' in config:
            raise Exception("Need trakt config client_id, client_secret and redirect_uri")

        self.trakt = config['trakt']

        for require in required:
            if not require in self.trakt:
                raise Exception("Need " + require + " in trakt config")

        super(Trakt, self).__init__(config, {
            "Content-type": "application/json",
            "trakt-api-key": self.trakt['client_id'],
            "trakt-api-version": "2"
        })

        print self.trakt
        
        self.loadTraktTokens()
        
        if not self.isAuthenticated():
            self.authenticate()

        if self.needsToRefreshToken():
            print "refreshing token..."
            self.refreshAccessToken()

    def needsToRefreshToken(self):
        return self.trakt['expires_at'] < time.time()

    def loadTraktTokens(self):
        try:
            print self.config.config
            print os.path.join(self.config['root'], '.trakt.yaml')
            f = open(os.path.join(self.config['root'], '.trakt.yaml'))
            tokens = yaml.load(f)
            f.close()

            self.trakt['access_token'] = tokens['access_token']
            self.trakt['refresh_token'] = tokens['refresh_token']
            self.trakt['expires_at'] = tokens['expires_at']

        except IOError:
            pass

    def saveTraktTokens(self):
        try:
            f = open(os.path.join(self.config['root'], '.trakt.yaml'), 'w+')
            tokens = {
                "access_token": self.trakt["access_token"],
                "refresh_token": self.trakt["refresh_token"],
                'expires_at': self.trakt['expires_at']
            }
            f.write(yaml.dump(tokens))
            f.close()
        except IOError:
            print "Couldn't save trakt tokens"


    def isAuthenticated(self):
        print self.trakt
        return "access_token" in self.trakt or "refresh_token" in self.trakt

    def authenticate(self):
        print "Open " + self.trakt['pin_url']
        pin = raw_input("Enter 8 digit pin:")
        self.getAccessToken(pin)

    def getAccessToken(self, pin):
        url = self.constructUrl("token")
        body = {
            "code": pin,
            "client_id": self.trakt["client_id"],
            "client_secret": self.trakt["client_secret"],
            "redirect_uri": self.trakt["redirect_uri"],
            "grant_type": "authorization_code"
        }
        print url
        print body
        resp, content = self.httprequest(url, "POST", body)
        
        content = json.loads(content)
        print content
        if not "access_token" in content or not "refresh_token" in content:
            print "something wrong..."

        self.trakt['access_token'] = content['access_token']
        self.trakt['refresh_token'] = content['refresh_token']
        self.trakt['expires_at'] = content['created_at'] + content['expires_in']

        self.saveTraktTokens()

    def refreshAccessToken(self):
        url = self.constructUrl("token")
        body = {
            "refresh_token": self.trakt["refresh_token"],
            "client_id": self.trakt["client_id"],
            "client_secret": self.trakt["client_secret"],
            "redirect_uri": self.trakt["redirect_uri"],
            "grant_type": "refresh_token"
        }

        print url, body
        resp, content = self.httprequest(url, "POST", body)

        content = json.loads(content)
        print content
        if not "access_token" in content or not "refresh_token" in content:
            print "something wrong..."

        self.trakt["access_token"] = content["access_token"]
        self.trakt["refresh_token"] = content["refresh_token"]

        self.saveTraktTokens()
        


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
            "hd": hd,
            "comments": "",
            "genre": ""
        }

        url = self.constructUrl("episode", {"show": name, "season": season, "episode": episode})
        resp, content = self.httprequest(url, "GET")
        print url
        
        content = json.loads(content)
        
        if not "status" in content:

            serie['season'] = content['season']
            serie['episode'] = content['number']
            serie['desc'] = content['overview'].replace('"', "'")
            serie['epName'] = content['title'].replace('"', "'")
        
            serie['year'] = datetime.datetime.strptime(content['first_aired'], "%Y-%m-%dT%H:%M:%S.%fZ").isoformat()
            
            serie['id'] = content['ids']['tvdb']

            # Get the season specific stuff, genres, poster, nrOfEpisodes
            url = self.constructUrl("seasons", {"show": name})
            resp, content = self.httprequest(url, "GET")            
            content = json.loads(content)
            
            if not "status" in content:
                for s in content:
                    print s
                    if int(serie['season']) == int(s['number']):
                        serie['poster'] = s['images']['poster']['full']
                        serie['nrOfEpisodes'] = s['episode_count']
                        break
        else:
            print "no data"

        return serie

    def getMovieInfo(self, name):
        url = self.constructUrl("movie", [name])
        print url
        resp, content = self.httprequest(url, "GET")
        content = json.loads(content)
        if not "status" in content:
            print content

    def getArtwork(self, serie, season):
        name = serie['name'] if "name" in serie else serie
        url = self.constructUrl("seasons", {"show": name})
        print url
        image = False
        resp, content = self.httprequest(url, "GET")
        content = json.loads(content)
        if not "status" in content:
            for s in content:
                if int(s['number']) == int(season):
                    image = s['images']['poster']['full']
                    break
        
        if image:
            resp, content = self.httprequest(image, "GET")
            if "status" in resp and resp['status'] == '200':
                print "downloading artwork"
                with open("art.jpg", "wb") as f:
                    f.write(content)


    def constructUrl(self, type, params={}):
        url = self.url[type]
        print url
        for key, value in params.items():
            url = url.replace("{"+key+"}", value)
        print url
        return url.replace(" ", "-")
