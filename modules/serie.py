import re

class Serie(object):
    def __init__(self,config):
        self.config = config

    def parseFilename(self, filename=False):
        if not filename:
            self.filename = self.config['filename']
        pattern = "'^(.+)\.(S?([0-9]|[0-9]){1,2})(E?([0-9]|[0-9]){1,2})(\.|-).*$'i"
        pattern = r"^(?P<name>(.*))\.(?:S)(?P<season>([0-9])*)(?:E)(?P<episode>([0-9])*)"
        matches = re.search(pattern, self.filename)
        self.name = matches.group("name")
        self.season = matches.group("season")
        self.episode = matches.group("episode")
