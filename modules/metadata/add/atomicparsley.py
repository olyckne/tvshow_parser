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