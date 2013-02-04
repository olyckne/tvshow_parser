import os
class File(object):

    def __init__(self, config):
        self.config = config

    def checkIfVideo(self):
        formats = ["mkv", "avi", "mp4", "m4v"]
        extension = os.path.splitext(self.config['file']['name'])[1][1:]

        return extension in formats


