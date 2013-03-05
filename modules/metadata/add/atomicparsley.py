from ..metadata import *
from subprocess import Popen, PIPE
import os


class Atomicparsley(Metadata):

    def __init__(self, config):
        self.__atomicparsley__ = False
        for path in os.getenv("PATH").split(os.pathsep):
            path = os.path.join(path, "AtomicParsley")
            if os.access(path, os.X_OK):
                self.__atomicparsley__ = path

        if not self.__atomicparsley__:
            raise Exception("AtomicParsley not found?! Exiting")
            sys.exit(1)

        super(Atomicparsley, self).__init__(config)



    def addMetadata(self, metadata, file=False):
        print metadata

        if not file:
            file = self.config['temp'] if 'temp' in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        cmd = self.__atomicparsley__ + " " + file + " -W "
        cmd = cmd + "--stik 'TV Show'"

        print cmd

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

        out, err = p.communicate()

        print out, err