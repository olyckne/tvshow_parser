from convert import *
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
        tracks = []
        tracks.append(self.extractVideo())
        tracks.append(self.extractAudio())

        if not self.type['audio'] == "m4a":
            tracks.insert(1, self.convertAudio(tracks[1], to='m4a'))
#        if not self.type['video'] == "h264":
#            newVideo = self.convertVideo(to="m4v")
#
#        if "sub" in self.config and os.path.isfile(self.config['sub']):
#            tracks.append(self.config['sub'])

        self.mergeTracks(tracks)

    def extractAudio(self, file=False):
        print "\n\n extract audio..."
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], self.config['file']['name'])

        self.type['audio'] = self.getMediaType("audio")

        outFile = "audio." + self.type['audio'] if self.type['audio'] else "ac3"
        cmd = self.__ffmpeg__ + " -i " + file + " -dn -acodec copy " + outFile
        out, err = self.__exec__(cmd)

        print out, err
        return outFile

    def extractVideo(self, file=False):
        print "\n\n exracts video..."
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], self.config['file']['name'])

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
        print err
        pattern = r"( )*(Stream) (#[0-9]:[0-9](\(.*\))?:) (" + type + ":) (?P<type>([A-Za-z0-9])*)"
        matches = re.search(pattern, value)

        if matches and "type" in matches.groupdict():
            return matches.group("type")
        return False

    def convertAudio(self, file=False, to='m4a'):
        print "\n\n converts audio..."
        codec = "libfdk_aac" if to == "m4a" else to
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], 'audio*')
        print file

        outFile = "audio." + to
        out, err = self.__exec__(self.__ffmpeg__ + " -i " + file + " -acodec " + codec + " -b:a 384k " + outFile)

        print out, err

        return outFile

    def addTrack(self, type, fileToAdd, file=False):
        print "\n\n adding track..."
        type = type.title()
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        print file
        cmd = self.__ffmpeg__ + " -i "
        if os.path.isfile(file):
            cmd = cmd + file + " -i "
        cmd = cmd + fileToAdd
        cmd = cmd + " -acodec copy -vcodec copy"
        cmd = cmd + " -y " + file

        print cmd
        out, err = self.__exec__(cmd)

        print out, err

    def mergeTracks(self, tracks, file=False):
        print "\n\n merging..."
        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        cmd = self.__ffmpeg__
        for track in tracks:
            cmd = cmd + " -i " + track
        cmd = cmd + " -vcodec copy -acodec copy -scodec copy -y"
        for i in range(len(tracks)):
            cmd = cmd + " -map " + str(i) + ":0"
        cmd = cmd + " " + file

        print cmd + "\n\n"
        out, err = self.__exec__(cmd)

        print out, err
