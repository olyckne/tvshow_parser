import abc
from subprocess import Popen, PIPE
from qtfaststart import processor
from qtfaststart.exceptions import FastStartException
import os


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

    def optimize(self, file=False):

        if not file:
            file = self.config['temp'] if "temp" in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])
        try:
            processor.process(file, file)
        except FastStartException:
            # A log message was printed, so exit with an error code
            raise SystemExit(1)
