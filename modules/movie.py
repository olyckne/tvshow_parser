import re


class Movie(object):
    def __init__(self, config):
        self.config = config

    def parseFilename(self, filename=False):
        print filename
