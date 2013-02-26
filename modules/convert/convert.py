import abc
from subprocess import Popen, PIPE


class Convert(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def convert(self):
        pass

    def __exec__(self, cmd):
        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

        return p.communicate()
