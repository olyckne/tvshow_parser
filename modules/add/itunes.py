from add import *
import subprocess
import re
import os
import shutil


class Itunes(Add):

    def add(self, file):
        if "itunes" in self.config:
            if self.shouldAddDirect():
                if self.addDirect(file):
                    return True
            else:
                return self.moveToPath(file)

        return False


    def shouldAddDirect(self):
        return "addDirect" in self.config['itunes'] and self.config['itunes']['addDirect']

    def addDirect(self, file):
        cmd = self.getDirectCmd(file)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (standardout, junk) = res.communicate()
        if not junk:
            if re.search(r"(file track id [0-9]+ of library playlist id [0-9]+ of source id [0-9]+)", standardout):
                return True
        return False

    def getDirectCmd(self, file):
        return '/usr/bin/osascript -e "tell application \\"iTunes\\" to add POSIX file \\"' + file + '\\""'

    def moveToPath(self, file):
        if "path" in self.config['itunes']:
            path = self.config['itunes']['path']
        if path[0] == '~':
            path = os.path.expanduser(path)
        if os.path.exists(path):
            if os.path.isfile(file):
                try:
                    parentPath = os.path.dirname(os.path.dirname(path+'/'))
                    print parentPath
                    print path
                    print file
                    shutil.copy(file, parentPath)
                    shutil.move(os.path.join(parentPath, os.path.basename(file)), path)
                except EnvironmentError as e:
                    raise e
                    return False
                else:
                    return True
