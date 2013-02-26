from convert import *
import os
import re


class Ffmpeg(Convert):

    def __init__(self, config):
        self.__ffmpeg__ = False
        for path in os.getenv("PATH").split(os.pathsep):
            path = os.path.join(path, "ffmpeg")
            if os.access(path, os.X_OK):
                self.__ffmpeg__ = path

        if not self.__ffmpeg__:
            raise Exception("ffmpeg not found?! Exiting")
            sys.exit(1)

        super(Ffmpeg, self).__init__(config)

    def convert(self):
        self.extractAudio()
        self.extractVideo()

    def extractAudio(self, file=False):
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        print "extracting audio..."
        audio = self.getMediaType("audio")

        print audio
        cmd = self.__ffmpeg__ + " -i " + file + " -dn -acodec copy audio." + audio if audio else "ac3"
        out, err = self.__exec__(cmd)

        print out, err

    def extractVideo(self, file=False):
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        print "extracting video..."
        value = self.getMediaType("video")

        print value
        cmd = self.__ffmpeg__ + " -i " + file + " -an -vcodec copy video." + value if value else "h264"
        out, err = self.__exec__(cmd)
        print out, err

    def getMediaType(self, type, file=False):
        type = type.title()
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        out, err = self.__exec__(self.__ffmpeg__ + " -i " + file)

        value = out if out else err
        pattern = r"( )*(Stream) (#[0-9]:[0-9](\(.*\))?:) (" + type + ":) (?P<type>([A-Za-z0-9])*)"
        matches = re.search(pattern, value)

        if matches and "type" in matches.groupdict():
            return matches.group("type")
        return False
