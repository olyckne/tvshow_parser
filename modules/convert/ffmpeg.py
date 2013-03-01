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
        self.type = {}
        super(Ffmpeg, self).__init__(config)

    def convert(self):
        origVideo = self.extractVideo()
        origAudio = self.extractAudio()
#        if not self.type['audio'] == "m4a":
#            newAudio = self.convertAudio(to='m4a')

    def extractAudio(self, file=False):
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], self.config['file']['name'])

        print "extracting audio..."
        self.type['audio'] = self.getMediaType("audio")

        outFile = "audio." + self.type['audio'] if self.type['audio'] else "ac3"
        cmd = self.__ffmpeg__ + " -i " + file + " -dn -acodec copy " + outFile
        out, err = self.__exec__(cmd)

        print out, err
        return outFile

    def extractVideo(self, file=False):
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], self.config['file']['name'])

        print "extracting video..."
        self.type['video'] = self.getMediaType("video")

        self.type['video'] = self.type['video'] if not self.type['video'] == "h264" else "m4v"

        outFile = "video." + self.type['video'] if self.type['video'] else "m4v"
        cmd = self.__ffmpeg__ + " -i " + file + " -an -vcodec copy " + outFile
        out, err = self.__exec__(cmd)
        print out, err

        return outFile

    def getMediaType(self, type, file=False):
        type = type.title()
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], self.config['file']['name'])

        out, err = self.__exec__(self.__ffmpeg__ + " -i " + file)

        value = out if out else err
        pattern = r"( )*(Stream) (#[0-9]:[0-9](\(.*\))?:) (" + type + ":) (?P<type>([A-Za-z0-9])*)"
        matches = re.search(pattern, value)

        if matches and "type" in matches.groupdict():
            return matches.group("type")
        return False

    def convertAudio(self, file=False, to='m4a'):
        codec = "libfdk_aac" if to == "m4a" else to
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], 'audio*')
        print file

        outFile = "audio." + to
        out, err = self.__exec__(self.__ffmpeg__ + " -i " + file + " -acodec " + codec + " -b:a 384k " + outFile)

        print out, err

        return outFile

        print out, err


