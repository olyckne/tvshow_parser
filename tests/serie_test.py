from modules import serie

class TestSerie():

    def setup(self):
        self.config = {"file": {}}
        self.media_handler = serie.Serie(self.config)
    def testParseFilename(self):
        "It parses as filename"

        self.media_handler.parseFilename('TV.Show.S01E01.720p.mkv')
        assert self.media_handler.name == 'TV Show'
        assert self.media_handler.season == '1'
        assert self.media_handler.episode == '1'
        assert self.media_handler.hd == True

        self.media_handler.parseFilename('TV.Show.01x02.mkv')
        assert self.media_handler.name == 'TV Show'
        assert self.media_handler.season == '1'
        assert self.media_handler.episode == '2'
        assert self.media_handler.hd == False
