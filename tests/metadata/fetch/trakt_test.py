from modules.metadata.fetch import trakt
from nose.tools import assert_raises
import time

class TestTrakt():

    config = {
            "trakt": {
            "client_id": "xxx",
            "client_secret": "xxx",
            "pin_url": "https://trakt.tv/pin/xxxx",
            "redirect_uri": "bla",
            "access_token": "bla",
            "refresh_token": "bla",
            "expires_at": time.time()+10000
        }
    }
    
    def testInit(self):
        assert_raises(Exception, trakt.Trakt, {})
        config = {
            "trakt": {
                "client_id": "xxx", 
                "client_secret": "xxx",
                "pin_url": "https://trakt.tv/pin/xxxx"
            }
        }
        assert_raises(Exception, trakt.Trakt, config)

    def testConstructUrl(self):
        traktTV  = trakt.Trakt(self.config)
        assert traktTV.constructUrl('episode', {"show": "TV Show", "season": "1", "episode": "1"}) == 'https://api-v2launch.trakt.tv/shows/TV-Show/seasons/1/episodes/1?extended=full'

    def testIsAuthenticated(self):
        traktTV = trakt.Trakt(self.config)

        assert traktTV.isAuthenticated() == True
