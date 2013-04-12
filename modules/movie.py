import re


class Movie(object):
    def __init__(self, config):
        self.config = config

    def parseFilename(self, filename=False):
        if not filename:
            if "metadata" in self.config['file'] and \
            "filename" in self.config['file']['metadata']:
                self.filename = self.config['file']['metadata']['filename']
            else:
                self.filename = self.config['file']['name']
        pattern = r"^(?P<name>(.*))\.(?P<year>([0-9])*)"
        matches = re.search(pattern, self.filename)

        print matches.group("name")
        print matches.group("year")
