import subliminal
import os
import shutil


class Subtitle(object):

    def __init__(self, config):
        self.config = config

    def getSubtitle(self):
        if not "sub" in self.config or not os.path.isfile(self.config['sub']):
            name = os.path.splitext(self.config['file']['name'])[0]
            file = os.path.join(self.config['file']['path'], name + ".srt")
            if os.path.isfile(file):
                print "found file. copying to temp"
                shutil.copy(file, self.config['temp'])
                self.config['sub'] = os.path.join(self.config['temp'], name + ".srt")
            else:
                print "trying to download subtitle"
                file = self.config['file']['name']
                lang = self.config['language']['subtitle']
                cache = self.config['temp']['path'] if "temp" in self.config else self.config['file']['path']
                self.config['sub'] = subliminal.download_subtitles(file, languages=lang, cache_dir=cache)
                if self.config['sub'].items() and \
                    len(self.config['sub'].items()[0]) >= 2 and \
                    len(self.config['sub'].items()[0][1]):
                        # Get filename
                        self.config['sub'] = self.config['sub'].items()[0][1][0].path
                else:
                    self.config['sub'] = None
        return self.config['sub']
