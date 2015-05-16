import re


class Serie(object):
    def __init__(self, config):
        self.config = config

    def parseFilename(self, filename=False):
        if not filename:
            if "metadata" in self.config['file'] and \
            "filename" in self.config['file']['metadata']:
                self.filename = self.config['file']['metadata']['filename']
            else:
                self.filename = self.config['file']['name']
        else:
            self.filename = filename
#        pattern = "'^(.+)\.(S?([0-9]|[0-9]){1,2})(E?([0-9]|[0-9]){1,2})(\.|-).*$'i"
#
#        #
#        # TV.Show.Name.SxxExx.mkv
        pattern = r"^(?P<name>(.*))\.(?:[Ss])(?P<season>([0-9])*)(?:[Ee])(?P<episode>([0-9])*)"
        matches = re.search(pattern, self.filename)
        if not matches:
            ## TV.Show.Name.01x01.mkv
            pattern = r"^(?P<name>(.*))\.(?P<season>([0-9])*)(?:x)(?P<episode>([0-9])*)"

            matches = re.search(pattern, self.filename)

        if matches:
            self.name = matches.group("name")
            self.name = re.sub(r"[._-]", " ", self.name)
            self.season = matches.group("season")
            if not int(self.season) == 0 or not int(self.season) == 00:
                self.season = self.season.lstrip("0")
            self.episode = matches.group("episode")
            if not int(self.episode) == 0 or not int(self.season) == 0:
                self.episode = self.episode.lstrip("0")
        else:
            self.name = self.filename
            self.season = 0
            self.episode = 0

        if re.search(r"(720|1080)p", self.filename):
            self.hd = True
        else:
            self.hd = False

        # Check if name is in config and we should use that instead of the parsed one
        if "metadata" in self.config['file']:
            if self.name in self.config['metadata']:
                self.name = self.config['metadata'][self.name]

        # Check if user passed args to use for metadata
        if "metadata" in self.config['file']:
            metadata = self.config['file']['metadata']
            self.name = metadata['name'] if 'name' in metadata else self.name
            self.season = metadata['season'] if 'season' in metadata else self.season
            self.episode = metadata['episode'] if 'episode' in metadata else self.episode
            if "hd" in metadata:
                self.hd = True if metadata["hd"].lower() in ["true", "1", "yes"] else False

