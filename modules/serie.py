import re


class Serie(object):
    def __init__(self, config):
        self.config = config
        self.season = 0
        self.episode = 0
    
    def parseFilename(self, filename):
        # TV.Show.Name.SxxExx.mkv
        pattern = r"^(?P<name>(.*))\.(?:[Ss])(?P<season>([0-9])*)(?:[Ee])(?P<episode>([0-9])*)"
        matches = re.search(pattern, filename)
        if not matches:
            ## TV.Show.Name.01x01.mkv
            pattern = r"^(?P<name>(.*))\.(?P<season>([0-9])*)(?:x)(?P<episode>([0-9])*)"
            matches = re.search(pattern, filename)

        
        parsedData = {}
        if matches:
            parsedData['name'] = re.sub(r"[._-]", " ", matches.group("name"))

            parsedData['season'] = matches.group("season")
            if not int(parsedData['season']) == 0 or not int(parsedData['season']) == 00:
                parsedData['season'] = parsedData['season'].lstrip("0")
            parsedData['episode'] = matches.group("episode")
            if not int(parsedData['episode']) == 0 or not int(parsedData['episode']) == 0:
                parsedData['episode'] = parsedData['episode'].lstrip("0")
            parsedData['hd'] = True if re.search(r"(720|1080p)", filename) else False

        return parsedData

    def parse(self, filename):
        self.filename = filename
        self.name = self.filename


        matches = self.parseFilename(self.filename)

        if matches:
            self.name = matches['name']
            self.season = matches['season']
            self.episode = matches['episode']
            self.hd = matches['hd']

        # Check if user passed args to use for metadata
        if self.passedArgs():
            self.usePassedArgs()

        # Check if name is in config and we should use that instead of the parsed one
        if self.isNameInConfig(self.name):
            self.name = self.getNameFromConfig(self.name)


    def passedArgs(self):
        return "metadata" in self.config['file'] and self.config['file']['metadata'] != {}

    def usePassedArgs(self):
        metadata = self.config['file']['metadata']
        self.name = metadata['name'] if 'name' in metadata else self.name
        self.season = metadata['season'] if 'season' in metadata else self.season
        self.episode = metadata['episode'] if 'episode' in metadata else self.episode
        if "hd" in metadata:
            self.hd = True if metadata["hd"].lower() in ["true", "1", "yes"] else False

    def isNameInConfig(self, name):
        return "metadata" in self.config and name.lower() in map(str.lower, self.config["metadata"])

    def getNameFromConfig(self, name):
        return self.config['metadata'][name.lower()] if self.isNameInConfig(name) else name
