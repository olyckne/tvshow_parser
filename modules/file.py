import os
import tempfile
import shutil
import sys


class File(object):

    videoFormats = ["mkv", "avi", "mp4", "m4v"]

    def __init__(self, config):
        self.config = config

    def isVideo(self):
        extension = os.path.splitext(self.config['file']['name'])[1][1:]

        return extension in self.videoFormats



    def moveToTemp(self):
        self.path = tempfile.mkdtemp()

        filepath = ""
        if self.config['file']['path']:
            filepath = self.config['file']['path'] + "/"

        filepath += self.config['file']['name']

        filesize = os.stat(filepath).st_size
        copied = 0
        source = open(filepath, "rb")
        target = open(self.path + "/" + self.config['file']['name'], "wb")
        while True:
            chunk = source.read(32768)
            if not chunk:
                break
            target.write(chunk)
            copied += len(chunk)
            sys.stdout.write("\r\r%d%%" % (copied * 100 / filesize))
            sys.stdout.flush()

        source.close()
        target.close()
        os.chdir(self.path)

    def removeTemp(self):
        if self.path and os.path.exists(self.path):
            shutil.rmtree(self.path)
