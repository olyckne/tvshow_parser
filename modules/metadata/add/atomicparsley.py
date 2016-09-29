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

        super(Atomicparsley, self).__init__(config)



    def addMetadata(self, metadata, file=False):
        print metadata

        if not file:
            file = self.config['temp'] if 'temp' in self.config else self.config['file']
            file = os.path.join(file['path'], file['name'])

        cmd = self.__atomicparsley__ + " " + file + " -W "
        cmd = cmd + "--stik 'TV Show'"

        print "\n\n"
        print metadata.keys()

        print "\n\n"
        comment = ", ".join(metadata['comments']) if not isinstance(metadata['comments'], basestring) else metadata['comments']
        comment = comment + "\n" + os.path.basename(self.config['file']['name'])
        epID = '%d%s' %(metadata['season'], str(metadata['episode']).rjust(2, '0'))
        
        tags = {
            "kind": " --stik '%s'" %('TV Show' if self.config['type'] == "TV" else "Movie"),
            "name": " --artist '%(data)s' --TVShowName '%(data)s'" %{"data": metadata['name']},
            "season": " --TVSeasonNum %d" %(metadata['season']),
            "episode": " --TVEpisodeNum %d" %(metadata['episode']),
            "title": ' --title "%s"' %(metadata['epName']),
            "epID": " --TVEpisode '%s'" %(metadata['id']),
            "album": " --album '%s, Season %d'" %(metadata['name'], metadata['season']),
            "track": " --tracknum %d/%d" %(metadata['episode'], metadata['nrOfEpisodes']),
            "year": " --year '%s'" %(metadata['year']),
            "desc": ' --description "%(data)s"' %{"data": metadata['desc']},
            "genre": " --genre '%s'" %(metadata['genre']),
            "comment": " --comment '%s'" %(comment)
        }
        if os.path.isfile('art.jpg'):
            tags['art'] = " --artwork art.jpg"

        for tag in tags:
            cmd = cmd + tags[tag]

        cmd = cmd + " --overWrite"

        p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)

        out, err = p.communicate()

        print out, err
