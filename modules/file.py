import os
import tempfile
import shutil
import sys
import zipfile
import rarfile

class File(object):

    videoFormats = ["mkv", "avi", "mp4", "m4v"]

    def __init__(self, config):
        self.config = config

    def isVideo(self, filename):
        extension = os.path.splitext(filename)[1][1:]

        return extension in self.videoFormats

    def findVideo(self):
        fullpath = self.config['file']['path'] + self.config['file']['name']
        files = False
        if os.path.isdir(fullpath):
            os.chdir(fullpath)
            files = {"path": os.getcwd(), "files": []}
            archive = False
            for file in os.listdir(files['path']):
                if zipfile.is_zipfile(file):
                    print "Unzip..."
                    zip = zipfile.ZipFile(file)
                    zip.extractall()
                    archive = True
                elif rarfile.is_rarfile(file):
                    try:
                        print "Unrar..."
                        rar = rarfile.RarFile(file)
                        rar.extractall()
                        archive = True
                    except rarfile.NeedFirstVolume:
                        pass
                self.config['file']['name'] = file
                if self.isVideo():
                    files['files'].append(file)
            if archive:
                allFiles = os.listdir(files['path'])
                for file in allFiles:
                    self.config['file']['name'] = file
                    if not file in files['files'] and self.isVideo():
                        files['files'].append(file)

        return files

    def moveToTemp(self):
        self.path = tempfile.mkdtemp()
        self.config['temp'] = {
            "path": self.path,
            "name": os.path.splitext(self.config['file']['name'])[0] + ".m4v"
        }

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

    def removeTemp(self):
        if self.path and os.path.exists(self.path):
            shutil.rmtree(self.path)

    def cdToTemp(self):
        os.chdir(self.path)
