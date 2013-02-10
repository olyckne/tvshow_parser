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
                self.config['sub'] = subliminal.download_subtitles(
                    os.path.join(self.config['temp'], self.config['file']['name']),
                    self.config['language']['subtitle'], cache_dir=self.config['temp'])

        return self.config['sub']
