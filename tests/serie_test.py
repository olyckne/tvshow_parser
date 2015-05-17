from modules import serie

class TestSerie():

    def testParseFilename(self):
        "It parses a filename"
        
        self.config = {"file": {}}
        self.serie = serie.Serie(self.config)

        parsed = self.serie.parseFilename('TV.Show.S01E01.720p.mkv')
        assert parsed['name'] == 'TV Show'
        assert parsed['season'] == '1'
        assert parsed['episode'] == '1'
        assert parsed['hd'] == True

        parsed = self.serie.parseFilename('TV.Show.01x02.mkv')
        assert parsed['name'] == 'TV Show'
        assert parsed['season'] == '1'
        assert parsed['episode'] == '2'
        assert parsed['hd'] == False

    def testPassedArgs(self):
        "It checks if user passed metadata arguments"

        self.config = {"file": {}}
        self.serie = serie.Serie(self.config)
        assert self.serie.passedArgs() == False

        config = {
            "file": {
                "metadata": {
                    "name" "A TV Show"
                }
            }
        }
        handler = serie.Serie(config)

        assert handler.passedArgs() == True

    def testUsePassedArgs(self):
        "It uses the passed metadata arguments"

        config = {
            "file": {
                "metadata": {
                    "name": "A TV Show",
                    "hd": "False"
                }
            }
        }
        handler = serie.Serie(config)
        handler.usePassedArgs()

        assert handler.name == "A TV Show"
        assert handler.hd == False

    def testParse(self):
        "It parses as filename"

        self.config = {"file": {}}
        self.serie = serie.Serie(self.config)

        self.serie.parse('TV.Show.S01E01.720p.mkv')
        assert self.serie.name == 'TV Show'
        assert self.serie.season == '1'
        assert self.serie.episode == '1'
        assert self.serie.hd == True

        self.serie.parse('TV.Show.01x02.mkv')
        assert self.serie.name == 'TV Show'
        assert self.serie.season == '1'
        assert self.serie.episode == '2'
        assert self.serie.hd == False

    def testIsNameInConfig(self):
        "It checks if shows name is in the config"

        config = {
                "metadata": {
                    "TV Show": "TV Show 2015"
                }
        }

        handler = serie.Serie(config)

        assert handler.isNameInConfig("TV Show") == True
        assert handler.isNameInConfig("A TV Show") == False

    def testGetNameFromConfig(self):
        "It gets the show name from config"

        config = {
            "metadata": {
                "TV Show": "TV Show 2015"
            }
        }

        handler = serie.Serie(config)

        assert handler.getNameFromConfig("TV Show") == "TV Show 2015" 
        assert handler.getNameFromConfig("Another TV Show") == "Another TV Show"

