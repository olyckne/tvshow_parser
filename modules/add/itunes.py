from add import *
import subprocess
import re
import os
import shutil


class Itunes(Add):

    def add(self, file):
        if "itunes" in self.config:
            if "addDirect" in self.config['itunes'] and self.config['itunes']['addDirect']:
                cmd = '/usr/bin/osascript -e "tell application \\"iTunes\\" to add POSIX file \\"' + file + '\\""'
                print cmd
                res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                (standardout, junk) = res.communicate()
                if not junk:
                    if re.search(r"(file track id [0-9]+ of library playlist id [0-9]+ of source id [0-9]+)", standardout):
                        return True
            else:
                print self.config['itunes']
                if "path" in self.config['itunes']:
                    path = self.config['itunes']['path']
                if path[0] == "~":
                    path = os.path.expanduser(path)
                if os.path.exists(path):
                    if os.path.isfile(file):
                        try:
                            shutil.copy(file, path)
                        except EnvironmentError:
                            return False
                        else:
                            return True
        return False
