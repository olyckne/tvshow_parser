import os
import tempfile
import shutil
import sys


class File(object):

    def __init__(self, config):
        self.config = config

    def checkIfVideo(self):
        formats = ["mkv", "avi", "mp4", "m4v"]
        extension = os.path.splitext(self.config['file']['name'])[1][1:]

        return extension in formats


    def moveToTemp(self):
        temp = self.config['temp']['path'] + self.config['file']['name'] + "/"

        if os.path.exists(temp):
            print "OK!"
        else:
            self.path = tempfile.mkdtemp()

        filepath = self.config['file']['path'] + "/" + self.config['file']['name']
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

